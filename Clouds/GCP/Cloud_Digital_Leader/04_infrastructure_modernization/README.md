# Infrastructure and Application Modernization

Every organization that has been operating for more than a few years carries a technology legacy: servers in data centers, applications built on older frameworks, databases running on hardware approaching end-of-life. This infrastructure was built to solve the problems of its time, and in many cases it solved them well. But the pace of business has changed, and infrastructure that once served as a competitive advantage has become a constraint.

Modernization is the process of removing that constraint — moving workloads off aging infrastructure, redesigning applications to take advantage of cloud capabilities, and adopting computing models that scale, adapt, and cost less to operate. It is rarely a single project with a clear end date. It is a continuous journey of improvement, with each step removing friction and opening new capabilities.

---

## The Case for Modernization
Legacy infrastructure imposes costs that extend far beyond the monthly data center bill. Aging systems require specialized knowledge that is increasingly difficult to hire for. Hardware refresh cycles demand large, infrequent capital expenditures. The process of making changes — deploying a new feature, scaling a service, responding to a security vulnerability — is slow and risky compared to what cloud-native architectures enable.

The most tangible cost is speed. Modern software organizations release updates continuously — dozens of times per day in some cases. Organizations running monolithic applications on on-premises infrastructure may take weeks or months to deploy the same change. In markets where customer expectations and competitive dynamics change rapidly, the ability to iterate quickly is a structural advantage, not a luxury.

**Infrastructure modernization** addresses the underlying compute, storage, and networking: moving virtual machines to the cloud, adopting managed database services, and eliminating the operational burden of physical hardware.

**Application modernization** addresses the software itself: decomposing monolithic codebases into independent services, adopting container-based deployment, and building for the cloud-native patterns — stateless design, automated scaling, continuous delivery — that make rapid iteration possible.

These two dimensions reinforce each other. Infrastructure modernization creates the platform; application modernization makes full use of it.

---

## Migration Strategy: Matching the Approach to the Workload
Moving a portfolio of applications to the cloud is not a uniform exercise. Different workloads have different characteristics, different levels of technical debt, different regulatory constraints, and different business priorities. A thoughtful migration assigns each workload to the strategy that best balances speed, cost, risk, and long-term benefit.

The industry has converged on a set of strategies, often referred to as the migration "R" framework:

**Retire** applies to applications that are no longer providing business value — duplicated systems, abandoned internal tools, or capabilities that have been superseded by a SaaS product. The most efficient migration is no migration at all.

**Retain** applies to applications that cannot or should not move — systems with unresolvable hardware dependencies, workloads subject to regulatory constraints that prohibit cloud hosting, or legacy systems where migration risk outweighs the benefit. These remain on-premises, at least for now.

**Rehost** — often called "lift and shift" — moves an application to cloud virtual machines with no changes to the code or architecture. The application runs identically to how it ran on-premises, just on Google's infrastructure. This approach delivers the fastest migration timeline and immediate infrastructure cost savings, even though it does not optimize the application for cloud capabilities.

**Replatform** makes targeted, pragmatic improvements during migration: replacing a self-managed database with a fully managed cloud database service, or moving from a bare-metal application server to a managed container platform. The application logic stays largely intact; the operational model improves meaningfully.

**Refactor** restructures significant portions of the application to adopt cloud-native patterns — breaking a monolith into microservices, containerizing workloads, redesigning for stateless operation and automated scaling. This requires substantial engineering investment but yields the greatest long-term operational and scalability benefits.

**Reimagine** rebuilds from scratch using cloud-native principles. Reserved for situations where the original design is so constrained that incremental improvement cannot deliver the required capabilities.

Most organizations apply the full spectrum across their application portfolio — retiring some, retaining a few, rehosting many, replatforming others, and selectively refactoring the applications where the investment is most justified.

---

## Modern Compute Paradigms
The cloud offers several distinct ways to run software, each suited to different types of workloads and representing different trade-offs between control, operational overhead, and cost.

### Virtual Machines
Virtual machines remain the most direct path from on-premises to cloud. A VM provides a complete operating system environment, isolated from other workloads on the same physical host. Organizations can run any software that runs on-premises, with full control over OS configuration, installed software, and resource allocation. Google Compute Engine provides VMs across a wide range of sizes, operating systems, and regions.

### Containers and Kubernetes
Containers package an application and all its dependencies into a portable, lightweight unit that runs consistently across environments — a developer's laptop, a staging cluster, a production environment in any cloud. Unlike VMs, containers share the host operating system rather than running a complete OS per instance, making them far more efficient in resource usage and startup time.

Kubernetes, the open-source container orchestration system originally created by Google, manages the deployment, scaling, and health of containerized applications. Google Kubernetes Engine (GKE) delivers a fully managed Kubernetes environment, handling the operational complexity of running the control plane while giving teams full control over how their workloads are deployed and scaled.

### Serverless
Serverless computing removes infrastructure entirely from the developer's concern. Code runs in response to events — an incoming HTTP request, a message on a queue, a file uploaded to storage — and the platform handles all provisioning, scaling, and operational management. Billing reflects actual compute time consumed, not reserved capacity.

Google Cloud Run deploys containerized applications in a fully managed serverless environment, scaling from zero to thousands of instances based on incoming traffic and back to zero when idle. Cloud Functions handles individual event-triggered functions without even requiring a container. App Engine provides a managed runtime for web applications with built-in versioning, traffic splitting, and autoscaling.

### Microservices Architecture
As organizations modernize their applications, many move from monolithic architectures — where the entire application is a single deployable unit — toward microservices, where the application is composed of small, independent services that each do one thing and communicate over APIs.

Microservices enable independent deployment: the team responsible for the payment service can release an update without coordinating with the teams responsible for the catalog service, the search service, or the recommendations service. They enable independent scaling: if only the checkout service is under heavy load during a sale, only that service needs additional capacity. They enable technology diversity: different services can use different programming languages, frameworks, and databases, each chosen for the specific requirements of that service.

---

## APIs: The Connective Tissue of Modern Systems
Application Programming Interfaces — APIs — are the mechanism by which software components communicate with each other. Every microservice exposes an API. Every cloud service is accessed through an API. Every integration between systems, whether internal or external, relies on APIs.

For organizations, APIs represent both an operational necessity and a strategic opportunity. Organizations that expose their capabilities and data as well-designed APIs can build partner ecosystems, enable new customer-facing products, and monetize data assets they already possess. The businesses most successfully operating in the API economy — those that have made their core capabilities available to external developers — have created platforms that grow through network effects.

Managing APIs at scale — applying consistent authentication, rate limiting, monitoring usage, and providing a developer experience — is the domain of API management platforms. Google Cloud's Apigee provides these capabilities across the full API lifecycle.

---

## Hybrid and Multi-Cloud Architectures
For many organizations, cloud adoption is not a clean cutover from one environment to another. Data residency requirements, regulatory obligations, the complexity of legacy system integrations, and the realities of phased migration mean that workloads run in multiple environments simultaneously — on-premises, on Google Cloud, and potentially on other cloud platforms.

Managing this complexity consistently — applying uniform security policies, maintaining visibility across environments, enabling workloads to communicate reliably — is the central challenge of hybrid and multi-cloud architecture. Google Kubernetes Engine Enterprise (GKE Enterprise) provides a control plane for managing containerized applications across all of these environments from a single interface, applying consistent configuration and policy regardless of where a workload physically runs.

---

## Topics in This Section

- [Cloud Modernization and Migration](4.1_cloud_modernization_and_migration.md) — migration strategies, the business case for modernization, and key terminology
- [Computing in the Cloud](4.2_computing_in_the_cloud.md) — virtual machines, containers, Kubernetes, autoscaling, load balancing, and how to choose between compute options
- [Serverless Computing](4.3_serverless_computing.md) — Cloud Run, App Engine, and Cloud Functions
- [Containers in the Cloud](4.4_containers_in_the_cloud.md) — how containers differ from VMs, microservices architecture, and GKE
- [The Value of APIs](4.5_the_value_of_apis.md) — APIs as business assets, the API economy, and Apigee
- [Hybrid and Multi-Cloud](4.6_hybrid_and_multi_cloud.md) — reasons for hybrid and multi-cloud strategies, and GKE Enterprise