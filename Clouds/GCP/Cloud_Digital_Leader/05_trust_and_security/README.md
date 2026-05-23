# Trust, Security, and Compliance with Google Cloud

Security has become one of the most consequential dimensions of operating a modern organization. A significant data breach does not only cost money in direct remediation — it erodes customer trust, invites regulatory scrutiny, triggers legal liability, and can permanently alter a company's competitive position. Ransomware attacks have shut down hospitals, disrupted fuel supply chains, and paralyzed city governments. Phishing campaigns have caused billion-dollar wire fraud losses. The threat landscape is sophisticated, continuously evolving, and indiscriminate in its targets.

Against this backdrop, the question is not whether to take security seriously, but how. Most organizations cannot match the security investment that a major cloud provider makes. Google's infrastructure security is developed by thousands of dedicated security engineers, refined through years of defending one of the most frequently attacked surfaces on the internet, and continuously updated as new threats emerge. Moving to Google Cloud does not eliminate an organization's security responsibilities — but it fundamentally changes the nature and scope of those responsibilities.

---

## Rethinking Security in the Cloud
Traditional enterprise security was built around the concept of a perimeter: a network boundary, enforced by firewalls, inside which everything was trusted and outside which everything was suspect. This model made sense when employees worked in offices on company networks and applications ran in company data centers. It is deeply insufficient for an environment where employees work from anywhere, applications run across multiple clouds, and data is accessed from every type of device.

The model that has replaced it — Zero Trust — operates from the opposite premise: nothing inside the network is trusted by default. Every user, every device, and every application must be continuously verified, authenticated, and authorized for each resource they access, regardless of where the request originates. Google was one of the pioneers of Zero Trust through its BeyondCorp initiative, which eliminated the internal corporate network as a trusted zone and moved all access controls to the application layer. The same principles are available to Google Cloud customers through products like Identity-Aware Proxy and BeyondCorp Enterprise.

---

## The Layers of Security
Security is most effective when it is not dependent on any single control. A layered approach — defense in depth — means that if one control is bypassed or fails, others remain in place. Google Cloud implements security at every layer of its stack.

### Physical and Hardware Security
Google designs and builds its own data centers, using purpose-built servers with custom security hardware. The Titan security chip, embedded in Google's servers and networking equipment, performs cryptographic verification of the boot sequence — ensuring that the software running on Google's infrastructure has not been tampered with. Physical access to data centers is controlled with multiple barriers: biometric authentication, security personnel, 24/7 video surveillance, and anti-tailgating measures.

When storage media is decommissioned, it is destroyed through a multi-step process — degaussing followed by physical shredding — before any components leave Google's custody. Data cannot be recovered from decommissioned Google hardware.

### Encryption
Google encrypts all customer data at rest and in transit by default, with no configuration required. This means that even in the unlikely event that someone gained unauthorized access to Google's storage systems, the data they found would be unreadable without the cryptographic keys.

**Data at rest** — stored in databases, object storage, backups — is encrypted with AES-256, one of the strongest symmetric encryption standards in use. Encryption happens at the storage layer, transparently, before data is written to disk.

**Data in transit** — moving between a user's browser and Google's servers, between Google services, or across Google's private network — is encrypted using TLS (Transport Layer Security). Traffic between Google data centers travels over Google's private fiber network, not the public internet, further reducing exposure.

**Data in use** — actively being processed in memory — is addressed by Confidential Computing, which encrypts data even while it is being operated on by the CPU. This protects against a class of attacks that target data during processing.

Organizations with specific compliance requirements can manage their own encryption keys through Cloud Key Management Service (Cloud KMS), providing an additional layer of control and auditability.

### Identity and Access Management
Controlling who can do what — and maintaining a clear record of what was done — is fundamental to cloud security. Google Cloud's Identity and Access Management (IAM) system provides fine-grained control over access to every resource.

**Authentication** establishes identity: who is making this request? Passwords remain common, but they are increasingly insufficient against phishing and credential stuffing attacks. Two-step verification (2SV) adds a second factor — a code from an authenticator app, a hardware security key — that an attacker cannot obtain by stealing a password alone. Google's data shows that 2SV prevents 99.9% of automated account takeover attacks.

**Authorization** determines what an authenticated identity is permitted to do. IAM policies bind roles (sets of permissions) to identities (users, groups, service accounts) on specific resources. The principle of least privilege — granting only the minimum permissions necessary for a task — limits the blast radius when an account is compromised.

**Auditing** records what was done. Cloud Audit Logs capture every administrative action, every data access, and every system event, creating an immutable record that supports forensic investigation, compliance verification, and anomaly detection.

### Network Security
Google Cloud Armor provides distributed denial-of-service (DDoS) protection and web application firewall (WAF) capabilities at the network edge — before malicious traffic reaches an organization's applications. Google's global network absorbs attack traffic at scale, with the infrastructure to handle the largest recorded DDoS attacks without impact to protected applications.

VPC (Virtual Private Cloud) networks provide software-defined network isolation between resources. Firewall rules control which resources can communicate with which others. Private connectivity options — Cloud VPN, Cloud Interconnect — enable organizations to connect their on-premises networks to GCP without exposing traffic to the public internet.

---

## The Shared Responsibility Model
Cloud security is a shared responsibility, and understanding where Google's responsibility ends and the customer's begins is essential for security planning and compliance.

Google is responsible for the security of the cloud — the physical infrastructure, the hardware, the hypervisor, the network, and the managed services' underlying layers. This responsibility is consistent, documented, and independently verified through third-party audits.

Customers are responsible for security in the cloud — what they deploy, how they configure it, who they grant access to, how they manage their data, and how they secure their applications. A misconfigured Cloud Storage bucket that exposes sensitive data to the public internet is a customer misconfiguration, not a Google failure. An IAM policy that grants overly broad permissions to too many users is a customer responsibility.

The boundary shifts based on the service model. In an IaaS environment, customers manage operating system security, application security, and data. In a SaaS environment like Google Workspace, Google manages the application and its security; customers are responsible for user access and data handling.

---

## Compliance and Regulatory Requirements
Operating in regulated industries — healthcare, financial services, government — imposes specific requirements on how data is stored, processed, and protected. Organizations must demonstrate to regulators, auditors, and customers that their controls meet these requirements.

Google Cloud holds a comprehensive set of third-party certifications and attestations — ISO 27001, SOC 1 and SOC 2, PCI DSS, FedRAMP, HIPAA — that verify its infrastructure meets the standards required to host regulated workloads. These certifications are maintained through continuous monitoring and periodic independent audits.

**Data residency** — controlling where data is physically stored — is a requirement for many organizations, driven by national regulations (GDPR in the EU, data localization laws in various countries) or contractual commitments. Google Cloud allows organizations to specify the regions where their data is stored, and Assured Workloads extends this with enforced controls on where data can be processed and who within Google can access it.

**Data sovereignty** addresses a related but distinct concern: which jurisdiction's laws govern the data. An organization operating under EU law must ensure that EU citizen data is not subject to conflicting legal demands from other jurisdictions. Google Cloud's transparency commitments — publishing reports on government data requests and committing to challenge overreaching legal demands — support customers' data sovereignty posture.

The Google Cloud Compliance Reports Manager provides customers with direct access to Google's audit reports and compliance documentation, enabling them to satisfy their own auditors and customers without the cumbersome process of requesting reports manually.

---

## Topics in This Section

- [Trust and Security in the Cloud](5.1_trust_and_security_in_the_cloud.md) — the modern threat landscape, how cloud security differs from on-premises, the CIA triad, and key security terminology
- [Google's Trusted Infrastructure](5.2_google_trusted_infrastructure.md) — Google's defense-in-depth approach, custom hardware, encryption, IAM, 2SV, Cloud Armor, and SecOps
- [Google Cloud's Trust Principles and Compliance](5.3_trust_principles_and_compliance.md) — Google's trust commitments, data sovereignty, data residency, transparency reports, and the Compliance Reports Manager