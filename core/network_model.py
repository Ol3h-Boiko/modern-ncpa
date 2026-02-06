import wmi
import pythoncom
import subprocess
import re

class NetworkAdapterModel:
    def get_ssid(self):
        try:
            output = subprocess.check_output("netsh wlan show interfaces", shell=True).decode('utf-8', errors='ignore')
            match = re.search(r'^\s*SSID\s*:\s*(.*)$', output, re.MULTILINE)
            if match:
                return match.group(1).strip()
        except:
            return None
        return None

    def format_speed(self, speed_bits):
        if not speed_bits:
            return "Unknown"
        try:
            speed = float(speed_bits)

            if speed >= 1_000_000_000:
                return f"{speed / 1_000_000_000:.1f} Gbps"
            elif speed >= 1_000_000:
                return f"{speed / 1_000_000:.0f} Mbps"
            return f"{speed} bps"
        except:
            return "Unknown"

    def get_all_adapters(self):
        try:
            pythoncom.CoInitialize()
            c = wmi.WMI()
            all_adapters = c.Win32_NetworkAdapter()

            data = []
            current_ssid = self.get_ssid()

            for adapter in all_adapters:
                if not adapter.NetConnectionID:
                    continue

                name_lower = (adapter.Name or "").lower()
                net_id_lower = (adapter.NetConnectionID or "").lower()

                is_wireless_type = False
                if any(x in name_lower for x in ["wi-fi", "wireless", "802.11", "bluetooth"]):
                    is_wireless_type = True
                if any(x in net_id_lower for x in ["wi-fi", "bluetooth"]):
                    is_wireless_type = True

                status_code = adapter.NetConnectionStatus
                status_text = "Disabled"

                if status_code == 2:
                    status_text = "Connected"
                elif status_code == 7:
                    if is_wireless_type:
                        status_text = "Not connected"
                    else:
                        status_text = "Network cable unplugged"

                is_wifi = False
                if adapter.Name and ("wi-fi" in adapter.Name.lower() or "wireless" in adapter.Name.lower()):
                    is_wifi = True

                display_status = status_text
                if is_wifi and status_code == 2 and current_ssid:
                    display_status = current_ssid

                ip_v4 = []
                ip_v6 = []
                subnet = "N/A"
                gateway = "N/A"
                dns = []
                raw_speed = adapter.Speed if status_code == 2 else 0

                try:
                    configs = adapter.associators(wmi_result_class='Win32_NetworkAdapterConfiguration')
                    if configs:
                        cfg = configs[0]
                        if cfg.IPEnabled:
                            if cfg.IPAddress:
                                for ip in cfg.IPAddress:
                                    if ':' in ip: ip_v6.append(ip)
                                    else: ip_v4.append(ip)

                            if cfg.IPSubnet: subnet = ", ".join(cfg.IPSubnet)
                            if cfg.DefaultIPGateway: gateway = ", ".join(cfg.DefaultIPGateway)
                            if cfg.DNSServerSearchOrder: dns = cfg.DNSServerSearchOrder
                except:
                    pass

                data.append({
                    "id": adapter.DeviceID,
                    "friendly_name": adapter.NetConnectionID,
                    "device_name": adapter.Name,
                    "status": display_status,
                    "is_connected": status_code == 2,
                    "mac": adapter.MACAddress,
                    "speed": self.format_speed(raw_speed),
                    "details": {
                        "ipv4": ", ".join(ip_v4) if ip_v4 else "Not configured",
                        "ipv6": ", ".join(ip_v6) if ip_v6 else "Not configured",
                        "subnet": subnet,
                        "gateway": gateway,
                        "dns": ", ".join(dns) if dns else "Automatic",
                        "driver": adapter.ServiceName or adapter.Name
                    }
                })

            return data

        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            pythoncom.CoUninitialize()