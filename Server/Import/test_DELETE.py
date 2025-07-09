import subprocess

def ping_ip(ip):
	# Ping the IP address using the system's ping command
	try:
		output = subprocess.check_output(['ping', '-c', '1', ip], stderr=subprocess.STDOUT, universal_newlines=True)
		return True
	except subprocess.CalledProcessError:
		return False

def ping_range(base_ip, start, end):
	# Iterate through the range of IPs
	for i in range(start, end + 1):
		ip = f"{base_ip}.{i}"
		if ping_ip(ip):
			print("yesyesyesyesyesyesyesyesyesyes")
			print(f"{ip} is reachable.")
			print("yesyesyesyesyesyesyesyesyesyes")
		else:
			print(f"{ip} is not reachable.")

if __name__ == "__main__":
	# Define your base IP (without the last octet) and the range you want to ping
	base_ip = "169.254.206"  # Example for a local network, adjust as needed
	start_ip = 1
	end_ip = 254

	# Ping the specified range of IPs
	ping_range(base_ip, start_ip, end_ip)
