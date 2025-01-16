# ESC4 Automation Workflow Script

This repository contains a Python script to automate the **ESC4 Workflow** using Certipy. It performs three main steps to exploit the vulnerability responsibly in a controlled environment. The script ensures efficient execution with retries, dynamic certificate handling, and enhanced logging.

## Features
- Automates the **ESC4 Workflow**.
- Uses Certipy to:
  - Make a certificate template vulnerable.
  - Request a certificate.
  - Authenticate using the certificate.
- Includes retry logic for robustness.
- Dynamically extracts the certificate file name from output.
- Uses colored logs for better visibility.

## Requirements
- **Python 3.x**
- Certipy installed and accessible in the system's PATH.
- Access to a target Active Directory Certificate Services (ADCS) environment.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```
2. Ensure Certipy is installed. You can install it using pip:
   ```bash
   pip install certipy
   ```
3. Run the script using Python 3.

## Usage

Run the script with the required parameters:

```bash
python esc4_automation.py \
  -t <template_name> \
  -ca <ca_server_name> \
  -ip <dc_ip> \
  -host <target_host> \
  -u <username> \
  -p <password> \
  -upn <upn> \
  -dns <dns_value> \
  -ns <ns_value>
```

### Arguments
- `-t, --template`: Template name to make vulnerable.
- `-ca, --ca-server`: Name of the Certificate Authority server.
- `-ip, --dc-ip`: IP address of the Domain Controller.
- `-host, --target-host`: DNS name of the target host.
- `-u, --user`: Username for authentication.
- `-p, --password`: Password for the user.
- `-upn, --upn`: UPN for the certificate request.
- `-dns, --dns`: DNS value for the certificate request.
- `-ns, --ns`: NS value for the certificate request.

## Output
The script performs the following steps:
1. **Make the template vulnerable:** Updates the template to allow exploitation.
2. **Request a certificate:** Requests a certificate from the CA server. If it fails, retries with debug mode.
3. **Authenticate using the certificate:** Authenticates using the generated PFX file.
> small but important note
> At the last step it will seem like the script is hanging. This is because certipy wants input from the user. Just wait 10 seconds and it will auto continue and give you the hash of the wanted user. 

Logs are color-coded for better clarity:
- **Green:** Successful operations.
- **Yellow:** Informational messages or retries.
- **Red:** Errors or failures.

## Troubleshooting
- Ensure Certipy is installed and configured correctly.
- Check if the target host and CA server are accessible.
- Verify that the credentials used have the required permissions.

## Notes
- This script is intended for ethical and authorized use only.
- Always ensure you have permission to test the environment.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

**Author**: [Your Name]  
**Version**: 1.0.0

