# in routes/pcap_analysis.py

from flask import Blueprint, request, jsonify
# FIX: Ensure all necessary layers and functions are imported from scapy.all
from scapy.all import rdpcap, IP, TCP, UDP, ICMP, DNSQR, sniff
import os
from collections import Counter

pcap_bp = Blueprint('pcap', __name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 

IP_PROTOS = {
    1: "ICMP", 6: "TCP", 17: "UDP", 41: "IPv6", 47: "GRE", 50: "ESP",
    51: "AH", 88: "EIGRP", 89: "OSPF", 132: "SCTP", 136: "UDP-Lite"
}
KNOWN_UDP_PORTS = {53, 67, 68, 69, 123, 161, 162, 500, 4500, 3389} 

@pcap_bp.route('/pcap-analysis', methods=['POST'])
def analyze_pcap():
    if 'file' not in request.files or not request.files['file'].filename.lower().endswith(('.pcap', '.pcapng')):
        return jsonify({"error": "Please upload a valid .pcap or .pcapng file."}), 400

    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        packets = rdpcap(filepath)
        total_packets = len(packets)
        
        protocol_counts = Counter()
        conversation_counts = Counter()
        security_findings = []
        dns_queries = []
        
        suspicious_udp_count = 0
        
        for packet in packets:
            if packet.haslayer(IP):
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst
                proto_num = packet[IP].proto
                protocol = IP_PROTOS.get(proto_num, f"IP Proto {proto_num}")
                
                protocol_counts[protocol] += 1
                key = tuple(sorted((src_ip, dst_ip))) 
                conversation_counts[key] += 1

                # --- Security Analysis Logic ---
                
                # TCP Checks (Cleartext)
                if packet.haslayer(TCP):
                    if packet.dport in [80, 21] or packet.sport in [80, 21]:
                        finding = f"Potential cleartext traffic (Port {packet[TCP].dport}) found. Check for exposed credentials/data."
                        if finding not in security_findings: security_findings.append(finding)

                # UDP/UDP-Lite Checks
                # FIX: Check for both standard UDP (17) and UDP-Lite (136) via proto_num
                if proto_num in [17, 136]:
                    
                    # Try to get the port numbers if the standard UDP layer is present
                    # This handles standard UDP (17) and may fail for some UDP-Lite (136) packets if they don't follow the standard layer structure
                    src_port = packet[UDP].sport if packet.haslayer(UDP) else None
                    dst_port = packet[UDP].dport if packet.haslayer(UDP) else None

                    if dst_port == 53 or src_port == 53:
                        if packet.haslayer(DNSQR):
                            query = packet[DNSQR].qname.decode('utf-8', 'ignore').rstrip('.')
                            if query and query not in dns_queries: dns_queries.append(query)
                    
                    # Flag UDP-Lite specifically as it can be suspicious/non-standard if not expected
                    if proto_num == 136:
                        finding = "⚠️ Protocol 136 (UDP-Lite) traffic detected. This is non-standard for general internet use and may indicate a specialized or covert data transfer."
                        if finding not in security_findings: security_findings.append(finding)


                    # Stricter Suspicious UDP Check (only run if we successfully got ports)
                    if src_port is not None and dst_port is not None:
                        is_known_port = (dst_port in KNOWN_UDP_PORTS) or (src_port in KNOWN_UDP_PORTS)
                        is_ephemeral_range = (dst_port > 49151) or (src_port > 49151)

                        if not is_known_port and not is_ephemeral_range:
                            suspicious_udp_count += 1
                
                # ICMP Checks (Ping Floods)
                if packet.haslayer(ICMP) and packet[ICMP].type == 8: # Echo Request
                    finding = "ICMP Echo Request traffic detected. Can be used for reconnaissance (ping sweeps)."
                    if finding not in security_findings: security_findings.append(finding)
        
        # --- Aggregated Findings ---

        # Lowered Suspicious UDP Threshold
        suspicious_threshold = max(5, total_packets * 0.02)
        if suspicious_udp_count > suspicious_threshold:
             finding = f"⚠️ High volume ({suspicious_udp_count} packets) of non-standard, non-ephemeral UDP traffic detected. Potential for DDoS or covert channel activity."
             security_findings.append(finding)

        # Check for single-source traffic flood/scan
        if total_packets > 100:
            source_ip_counts = Counter(packet[IP].src for packet in packets if packet.haslayer(IP))
            for ip, count in source_ip_counts.items():
                if count > total_packets * 0.5:
                    finding = f"🚨 Single source IP ({ip}) initiated {count} packets ({round(count/total_packets*100)}%). Potential for flooding or network scanning."
                    if finding not in security_findings: security_findings.append(finding)
        
        # Fallback if no specific findings
        if not security_findings:
            security_findings.append("No immediate high-risk security findings detected based on current rules.")
            
        os.remove(filepath)
        
        top_conversations = [
            {"src": conv[0], "dst": conv[1], "count": count}
            for conv, count in conversation_counts.most_common(10)
        ]
        
        protocol_summary = [
            {"protocol": proto, "count": count}
            for proto, count in protocol_counts.items()
        ]

        cia_analysis = {
            "confidentiality": "Analysis of unencrypted traffic (HTTP, FTP) and DNS queries can reveal confidential data.",
            "integrity": "Packet checksums can be validated to ensure data was not tampered with in transit.",
            "availability": "Detection of high-volume traffic (UDP/ICMP floods, single-source flooding) is key to mitigating DoS attacks on availability."
        }
        
        return jsonify({
            "message": f"Successfully analyzed {total_packets} packets.",
            "total_packets": total_packets,
            "security_findings": security_findings,
            "dns_queries": dns_queries[:20],
            "top_conversations": top_conversations,
            "protocol_summary": protocol_summary,
            "cia_analysis": cia_analysis
        })
        
    except Exception as e:
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({"error": f"PCAP analysis failed: {str(e)}"}), 500