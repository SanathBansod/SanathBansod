# Wazuh File Integrity Monitoring + Windows Sysmon — SOC Lab Guide

> **Focus:** Blue Team • SOC • SIEM • Endpoint Telemetry • File Integrity Monitoring  
> **Difficulty:** Beginner to intermediate  
> **Lab status:** Documentation and reproducible instructions. Complete the steps in your own isolated lab and add your own screenshots and validated results before claiming the detections were run.

---

## 1. Project Overview

This lab brings together two kinds of endpoint evidence:

- **Wazuh File Integrity Monitoring (FIM):** detects changes to selected files and directories, such as a file being added, modified, or deleted.
- **Windows Sysmon:** records detailed Windows system activity such as process creation, network connections, and selected file events, based on its configuration.

The SOC analyst uses the events to answer questions like:

- Which file changed, and when?
- Which user or process may be related to the change?
- Did an unexpected process start?
- Did the process create a network connection?
- Is the activity expected, suspicious, or still inconclusive?

**Important:** FIM and Sysmon provide telemetry, not automatic proof of an attack. You must validate events with context.

## 2. Lab Architecture

~~~text
                Isolated SOC Training Network
                           |
             +-------------+-------------+
             |                           |
             v                           v
     Linux endpoint                Windows endpoint
     Wazuh Agent                   Sysmon + Wazuh Agent
             |                           |
             +-------------+-------------+
                           |
                           v
                    Wazuh Manager
                           |
                           v
                Alerts / Event investigation
                           |
                           v
                Evidence and SOC incident note
~~~

You can use a separate Wazuh all-in-one lab VM and a Windows test VM. Keep the lab on a private/host-only virtual network where possible. Do not expose the manager dashboard or agent ports to the public internet.

## 3. Components in Simple English

| Component | Purpose |
|---|---|
| Wazuh Manager | Receives and analyzes agent events and produces alerts |
| Wazuh Agent | Collects supported telemetry from an endpoint |
| Wazuh FIM | Monitors configured paths for file changes |
| Windows Sysmon | Records detailed Windows process and network telemetry |
| Sysmon configuration | Controls which Sysmon events are collected |
| SOC analyst | Reviews evidence, checks context, documents findings, and decides next steps |

Wazuh and Sysmon are separate technologies. Installing Sysmon does not automatically guarantee that its events are forwarded into Wazuh. You must configure collection and validate that the Windows event channel reaches the manager.

## 4. Prerequisites and Safety

- A Wazuh manager installed using the current official Wazuh instructions.
- A supported Linux endpoint with a Wazuh agent.
- A Windows test VM with administrator access.
- Sysmon downloaded from the official Microsoft Sysinternals page.
- An isolated, authorized training environment.
- Sufficient disk and memory for your VMs.

Use a snapshot before changing endpoint monitoring configuration. Never test with real malware or use a company endpoint without permission. This guide uses benign file changes and ordinary process/network activity.

## 5. Deploy Wazuh

Wazuh installation instructions change across releases, so use the official Quickstart guide for the current version rather than copying an old installation command from a blog:

- [Wazuh Quickstart](https://documentation.wazuh.com/current/quickstart.html)
- [Wazuh agent installation guide](https://documentation.wazuh.com/current/installation-guide/wazuh-agent/index.html)

Suggested flow:

1. Create a dedicated lab VM for the Wazuh manager and dashboard.
2. Install Wazuh according to the official guide.
3. Confirm the dashboard opens from your private lab network.
4. Add the Linux endpoint using the current agent deployment instructions.
5. Add the Windows endpoint using the agent deployment instructions for Windows.
6. Verify both agents show as connected/active in the dashboard.
7. Record software versions, hostnames, private lab IP addresses, and installation time in your notes. Do not include secrets.

Do not continue to detection tests until the agent connection is confirmed.

## 6. Configure Wazuh File Integrity Monitoring

FIM compares the file state over time and alerts on configured changes. The paths monitored depend on the configuration and operating system.

Official reference: [Wazuh File Integrity Monitoring](https://documentation.wazuh.com/current/user-manual/capabilities/file-integrity/index.html)

### 6.1 Choose a safe test directory

On the Linux endpoint, create a lab-only directory:

~~~bash
mkdir -p ~/fim-lab
printf 'initial lab file\n' > ~/fim-lab/example.txt
ls -l ~/fim-lab
sha256sum ~/fim-lab/example.txt
~~~

Use this directory only for test data. Monitoring a user's home path may require configuration support specific to your Wazuh version.

### 6.2 Configure a monitored path

Use the supported FIM configuration method for your installed Wazuh version. On many Wazuh agent installations, the agent configuration file contains a syscheck/FIM section. Back up the file before modifying it, add the lab path using the syntax documented for your version, and restart the agent if required.

Do not blindly paste configuration into an arbitrary location. Check the official docs for the exact XML structure and whether the setting belongs on the manager or the agent.

After configuration:

1. Check that the agent remains connected.
2. Confirm the monitored path is listed in the active configuration.
3. Wait for the initial baseline scan or use the documented testing method.
4. Check manager/dashboard alerts for the test path.
5. If no event appears, inspect agent logs and validate that the path is included.

### 6.3 Generate benign FIM events

Perform these controlled changes on the lab Linux endpoint:

~~~bash
# Create a new text file
printf 'created for FIM testing\n' > ~/fim-lab/new-file.txt

# Modify the existing file
printf 'second line added at %s\n' "$(date -Is)" >> ~/fim-lab/example.txt

# Verify current hashes and contents
sha256sum ~/fim-lab/*.txt
cat ~/fim-lab/example.txt

# Delete only the test file created above
rm -- ~/fim-lab/new-file.txt
~~~

Expected observation: after the agent collects the change, FIM should report file activity for the monitored path. Exact event names and timing depend on configuration, version, and scan mode. Do not claim success until you see the event in the dashboard or alert data.

## 7. Install and Configure Windows Sysmon

Sysmon is a Windows system service and device driver that logs detailed system activity to the Windows Event Log. It does not analyze events as a SIEM by itself.

Official Microsoft reference: [Sysmon](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon)

### 7.1 Download

1. Open the official Microsoft Sysinternals Sysmon page.
2. Download the Sysmon archive from Microsoft.
3. Extract it into a lab tools folder, for example C:\LabTools\Sysmon.
4. Review the official documentation and the configuration you plan to use.

### 7.2 Choose a configuration carefully

A Sysmon XML configuration determines which event types are captured. Start with a reputable, reviewed configuration and read the filters before applying it. Broad event collection can create large volumes of telemetry.

Avoid downloading executable files or configuration files from untrusted sources. This guide does not embed an external XML configuration because rule selection should match the Windows version, lab goals, and current Sysmon schema.

### 7.3 Install Sysmon

Open PowerShell **as Administrator**, change to the folder that contains the extracted Sysmon executable, and use the official syntax documented for your downloaded release.

For example, when you have reviewed a configuration file named sysmonconfig.xml:

~~~powershell
cd C:\LabTools\Sysmon
.\Sysmon64.exe -accepteula -i .\sysmonconfig.xml
~~~

The exact executable name may differ between x64 and ARM64 packages. Use the file actually included in the download.

Check status and the available event channel:

~~~powershell
Get-Service Sysmon*
Get-WinEvent -ListLog *Sysmon* | Select-Object LogName, IsEnabled
~~~

Sysmon commonly writes to the Microsoft-Windows-Sysmon/Operational channel. Confirm the channel exists on your system instead of assuming the install succeeded.

### 7.4 Generate benign telemetry

Open Notepad from PowerShell:

~~~powershell
Start-Process notepad.exe
~~~

Then inspect recent Sysmon events:

~~~powershell
Get-WinEvent -LogName 'Microsoft-Windows-Sysmon/Operational' -MaxEvents 20 |
  Select-Object TimeCreated, Id, ProviderName, Message |
  Format-List
~~~

Expected result: depending on the installed configuration, process creation telemetry may appear. If no event is present, check Sysmon's service, channel, event filter, and logs.

For network telemetry, perform only an ordinary connection to a known lab or documentation endpoint that you are permitted to reach, then inspect the event channel. Sysmon network connection events are configuration-dependent. Do not assume every outbound connection is logged.

## 8. Forward Sysmon Events to Wazuh

Sysmon events need to be collected by the Windows Wazuh agent. The precise agent configuration can vary by Wazuh version, so follow the current official Windows eventchannel documentation:

- [Wazuh: Monitoring Windows event logs](https://documentation.wazuh.com/current/user-manual/capabilities/log-data-collection/configuration.html)

High-level workflow:

1. Confirm Sysmon writes events into the expected Windows event channel.
2. Configure the Windows Wazuh agent to collect the Sysmon Operational channel using the version-supported eventchannel syntax.
3. Restart the Wazuh agent if required by the documented configuration.
4. Verify the Windows agent returns to active status.
5. Generate another benign process event.
6. Search the Wazuh dashboard for the event and check its event ID, host, timestamp, and process details.
7. If the event is missing, troubleshoot each hop separately: Sysmon channel → agent configuration → agent connection → manager ingestion → dashboard filter.

**Never claim this integration is working until a real event is visible at the manager.** A successful Sysmon installation on Windows alone does not prove event forwarding.

## 9. Investigate Events Like a SOC Analyst

Use this simple process for each alert:

1. **Identify:** Capture rule/alert name, timestamp, hostname, and event ID.
2. **Validate:** Open the raw event and verify relevant fields.
3. **Scope:** Determine whether other endpoints or accounts show related events.
4. **Correlate:** Review nearby process, file, logon, and network events.
5. **Explain:** Write what the event shows without assuming intent.
6. **Decide:** Benign, suspicious/inconclusive, or confirmed incident based on the evidence.
7. **Document:** Record query, evidence file, limitations, and next steps.

### Sysmon fields worth reviewing

The available fields depend on the event ID and configuration. Look for:

- UtcTime / timestamp
- Computer / hostname
- Event ID
- Image / process path
- CommandLine, when captured
- User, when captured
- ParentImage and ParentCommandLine, when captured
- ProcessId and ParentProcessId
- DestinationIp and DestinationPort, for applicable network events
- Hashes, only when configured for collection

These fields can help answer what ran, under what context, and whether it made a network connection. A suspicious-looking command line alone is not proof of malicious behavior.

## 10. Lab Test Matrix

| Test | Action | Expected evidence | Result |
|---|---|---|---|
| FIM file creation | Create new file inside monitored lab path | File-added/integrity event | Fill after test |
| FIM file modification | Append text to the test file | Modification event | Fill after test |
| FIM file deletion | Delete only the test file | File-deleted event, when supported/configured | Fill after test |
| Sysmon process creation | Start Notepad | Process-creation event if included by config | Fill after test |
| Sysmon network connection | Make an approved benign connection | Network event if configured | Fill after test |
| Wazuh ingestion | Generate a new Sysmon event | Event visible in Wazuh dashboard | Fill after test |
| Correlation | Review process and nearby events | Documented timeline and assessment | Fill after test |

Do not mark a test as Passed until you have saved its evidence.

## 11. False Positives and Limits

- Legitimate installers and updates create many file changes.
- Browser updates and normal applications create processes and network connections.
- Build systems and developer tools can generate frequent file writes.
- A FIM alert says that a monitored file changed; it does not explain whether the change was authorized.
- Sysmon coverage depends on configuration. Missing events may mean the event type was not configured.
- Timestamp differences can complicate correlation.
- A single event rarely proves the complete intent of a process or user.

To reduce noise, monitor paths that matter, baseline normal activity, review event filters, and use the asset owner and change schedule as context.

## 12. Example SOC Investigation Note

Use this as a template, not as a claim that an event already occurred.

- **Case ID:** LAB-ENDPOINT-001
- **Host:** Record the actual lab hostname.
- **Time range:** Record the observed event-time window and timezone.
- **Trigger:** FIM file-change event or Sysmon process/network event.
- **Evidence:** Event ID, raw event excerpt, screenshot filename, and configuration version.
- **Analysis:** What changed or executed, user/process context, and related events.
- **False-positive checks:** Expected application, update, approved test, or change window.
- **Assessment:** Benign / suspicious-inconclusive / confirmed, with evidence.
- **Next step:** A specific validation or response action.
- **Limitations:** Missing telemetry, incomplete timestamps, or configuration gaps.

## 13. Evidence to Add to Your GitHub Portfolio

Only add screenshots captured from your own lab. Remove private IPs, usernames, tokens, hostnames, and other sensitive details when appropriate.

Suggested folder:

~~~text
evidence/
├── 01-wazuh-manager-and-agents.png
├── 02-fim-baseline.png
├── 03-fim-file-modification-alert.png
├── 04-sysmon-install-and-channel.png
├── 05-sysmon-process-event.png
├── 06-sysmon-event-visible-in-wazuh.png
└── 07-soc-investigation-timeline.png
~~~

For every screenshot, write one or two lines explaining what it proves. Do not add placeholder images and do not label untested steps as successful.

## 14. Practice Checklist

- [ ] Deploy Wazuh in an isolated lab using the official guide.
- [ ] Connect the Linux Wazuh agent.
- [ ] Connect the Windows Wazuh agent.
- [ ] Configure and verify a monitored FIM test directory.
- [ ] Generate and capture benign file create/modify/delete events.
- [ ] Install Sysmon from Microsoft's official source.
- [ ] Review Sysmon's configuration and event channel.
- [ ] Generate a benign process creation event.
- [ ] Configure the Wazuh agent to collect Sysmon events.
- [ ] Confirm a Sysmon event appears in Wazuh.
- [ ] Correlate evidence and write a SOC investigation note.
- [ ] Add real, sanitized screenshots and note any limitations.

## 15. Official References

- [Wazuh Quickstart](https://documentation.wazuh.com/current/quickstart.html)
- [Wazuh File Integrity Monitoring](https://documentation.wazuh.com/current/user-manual/capabilities/file-integrity/index.html)
- [Wazuh agent installation](https://documentation.wazuh.com/current/installation-guide/wazuh-agent/index.html)
- [Wazuh log data collection configuration](https://documentation.wazuh.com/current/user-manual/capabilities/log-data-collection/configuration.html)
- [Microsoft Sysmon documentation](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon)

---

**Portfolio honesty:** The guide is a lab plan until you run the configuration, confirm actual alerts, and collect your own evidence. Document successful tests separately from planned tests.
