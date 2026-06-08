# Microsoft Build 2026 — AI Announcement Index

_Auto-generated from public Microsoft Build 2026 session AI summaries (`build.microsoft.com/sessions`) and the public [`microsoft/Build26-news`](https://github.com/microsoft/Build26-news) repo. Re-run `python scripts/build_announcements.py` to refresh._

**224 announcement-signal items** mined across **8 topics**.

---

## Table of contents

- [AI Foundry](#ai-foundry) (83 items)
- [AI Infrastructure](#ai-infrastructure) (36 items)
- [Models](#models) (38 items)
- [Agents](#agents) (35 items)
- [Windows](#windows) (8 items)
- [Developer Tools](#developer-tools) (17 items)
- [Security + Governance](#security-governance) (3 items)
- [Other / Cross-cutting](#other--cross-cutting) (4 items)
- [Public Microsoft Build 2026 News (mirror)](#public-microsoft-build-2026-news-mirror)

---

## AI Foundry

_Microsoft Foundry — model catalog, Agent Service, Agent Framework, Foundry Toolkit, hosted agents, evaluations, fine-tuning_

### [BRK209] Japan Wrap-up Session
*Speakers:* Tadashi Okazaki  
[Session page](https://build.microsoft.com/en-US/sessions/BRK209) · [Video](https://medius.microsoft.com/Embed/video-nc/52082998-f4df-4fbb-8b20-f285b89fd486)

- The host explains that this 45-minute session will summarize the most important announcements from Build 2026 and present them clearly in Japanese for both livestream and local attendees (00:00:25–00:01:00).
- Experts from different fields at Microsoft Japan are introduced, and the first speaker, Executive Officer Okazaki, takes the stage to discuss Build 2026’s primary themes and announcements.
- Microsoft introduced new chipsets—Maia 200 and Cobalt 200—designed to enhance energy efficiency and AI workload processing across cloud and edge (00:05:29–00:06:04).
- Database breakthroughs, like Azure’s HorizonDB public preview and GPU-accelerated Fabric Data Warehouse, were showcased to strengthen enterprise-scale data operations (00:06:45–00:07:23).
- Yamamoto later discusses infrastructure scaling, highlighting Microsoft’s AI data center expansion focused on sustainability (Fairwater project), modernization support through Azure migration Copilot for mainframe-inclusive architectures, and the unveiling of Layfin—a framework that allows rapid AI-powered backend construction for production-ready applications (00:41:04–00:45:03).

### [BRK221] Idea to production-ready agent in seconds on AI-native runtime
*Speakers:* Simon Jakesch, Devanshi Joshi, Gopi Prashanth  
[Session page](https://build.microsoft.com/en-US/sessions/BRK221) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/8508448f-e225-4efd-b0ae-f89c2c2b91b5) · [Video](https://medius.microsoft.com/Embed/video-nc/8508448f-e225-4efd-b0ae-f89c2c2b91b5)

- The demo validates cold start under 100 milliseconds, sandbox persistence, connector inheritance, and strong network isolation—key architectural features of Azure Container Apps sandboxes in public preview.
- Product Announcements and Customer Use Cases: Transitioning back, Devanshi announces Azure Container Apps Sandboxes and Container Apps Express as a fast, isolated compute infrastructure executing workloads securely by default (00:27:00–00:29:00).
- Closing Insights and Q&A: Devanshi concludes the session summarizing that container apps and sandboxes are transforming AI agent production pipelines, now available in public preview (00:41:12).

### [BRK222] The honest practitioner's take on agentic AI on Kubernetes
*Speakers:* Lachie Evenson  
[Session page](https://build.microsoft.com/en-US/sessions/BRK222) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/9466a393-4172-4f0a-9849-190dab1b2623) · [Video](https://medius.microsoft.com/Embed/video-nc/9466a393-4172-4f0a-9849-190dab1b2623)

- He announces the public preview of "Anyscale on Azure" (00:25:15), a managed Ray service jointly developed with Anyscale, integrated with Azure’s identity and billing ecosystem.
- Announcements, Real-World Cases, and Closing Takeaways: Near 00:42:12, Lachlan announces new AKS features: Automatic node pools for simplified scaling, Azure Container Linux for secure, minimal OS footprints, AKS on bare metal for virtualization-free performance, and Fleet for managing multi-cluster topologies.

### [BRK224] PepsiCo’s blueprint for agentic AI
*Speakers:* Krunal Patel, Rishabh Saha, Bob Ward, Govanna Flores  
[Session page](https://build.microsoft.com/en-US/sessions/BRK224) · [Video](https://medius.microsoft.com/Embed/video-nc/95afb175-5c57-46c2-bd53-d67dda3d0888)

- They introduce the central challenge faced by key account managers (Cams): fragmented information across numerous systems and reports, described vividly between 00:09:04–00:10:00.

### [BRK230] Build smarter AI systems in Foundry as models and costs evolve
*Speakers:* Yina Arenas, Naomi Moneypenny, Sharmila Chockalingam  
[Session page](https://build.microsoft.com/en-US/sessions/BRK230) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/fb5d9581-c0ac-4290-9a9b-1fdcb98d6443) · [Video](https://medius.microsoft.com/Embed/video-nc/fb5d9581-c0ac-4290-9a9b-1fdcb98d6443)

- Yina introduces custom and rubric-based evaluation tools now available in Foundry (00:25:00), complementing built-in quality, safety, and compliance evaluators.
- She announces explicit prompt caching — a new Azure capability granting developers private, persistent caching layers to cut latency and token costs (00:32:00).

### [BRK231] Deploy. Observe. Learn. Reinforcement learning for production agents
*Speakers:* Alicia Frame, Omkar More, Long Chen  
[Session page](https://build.microsoft.com/en-US/sessions/BRK231) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/2e2fd0b4-5960-4c31-b9d2-946486fbbe5f) · [Video](https://medius.microsoft.com/Embed/video-nc/2e2fd0b4-5960-4c31-b9d2-946486fbbe5f)

- They outline the talk’s flow—covering fine-tuning, reinforcement learning, demos, and the upcoming low-level training API.
- Demo 3 – Low-Level API and Interactive Training: The third demo 00:33:10 introduces Foundry’s upcoming interactive training API—a low-level interface granting data scientists direct control over algorithms without managing GPU infrastructure.

### [BRK232] Post-Training and Deploying Open Source Reasoning Models in Foundry
*Speakers:* Vijay Aski, Manoj Bableshwar, Chris Lauren  
[Session page](https://build.microsoft.com/en-US/sessions/BRK232) · [Video](https://medius.microsoft.com/Embed/video-nc/b7ec6cc5-da1b-46e4-bce5-748e0e07c737)

- Evaluation dashboards reveal how smaller, post-trained models catch up with large proprietary ones in quality while reducing cost.
- A new API, tentatively called “Loom,” simplifies reinforcement and supervised tuning on CPUs without configuring GPU clusters.

### [BRK233] Software Defensibility in the era of AI coding
*Speakers:* Chip Huyen  
[Session page](https://build.microsoft.com/en-US/sessions/BRK233) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/6d282a65-465a-4585-a92b-ca528598b689) · [Video](https://medius.microsoft.com/Embed/video-nc/6d282a65-465a-4585-a92b-ca528598b689)

- The talk closes with excitement about upcoming robotics demonstrations and Chip’s vision of AI-enhanced physical systems still grounded by human purpose and defensible expertise 00:42:36.

### [BRK241] From prototype to production: build and run agents at scale
*Speakers:* Tina Schuchman, Jeff Hollan, Takuto Higuchi  
[Session page](https://build.microsoft.com/en-US/sessions/BRK241) · [Video](https://medius.microsoft.com/Embed/video-nc/af92c987-5029-4a5f-8a59-4a3931941ce5)

- Introduction and Vision for AI Agents: The video begins with Tina Schackman and Jeff Holland introducing themselves and outlining the session’s purpose—showing how to build, deploy, and operate enterprise-level AI agents using Microsoft Foundry (00:00:00–00:00:27).
- The Foundry Toolkit now generally available helps developers integrate tracing, evaluations, and best practices directly in the coding environment (00:09:54–00:10:04).
- Deploying and Hosting Enterprise Agents at Scale: Tina follows up announcing production-ready releases: Microsoft Agent Framework v1.0, Foundry Toolkit in VS Code, and upcoming Foundry hosted agents with secure sandbox isolation and long-running support (00:18:02–00:19:59).

### [BRK242] Turn your agents into action: Connect tools, APIs, and documents
*Speakers:* Ronak Chokshi, Joe Filcik, Maria Naggaga  
[Session page](https://build.microsoft.com/en-US/sessions/BRK242) · [Video](https://medius.microsoft.com/Embed/video-nc/e70ca1c3-f52b-4bcb-bc80-6e6afc4f5537)

- In Foundry, she uploads a reusable skill and introduces browser automation — a new capability for scraping and form filling built on Playwright (00:17:00–00:18:06).
- Content Understanding and Real-World Applications: Joe Flick takes over, introducing “Content Understanding” as the solution for agents handling complex multimodal content outside APIs such as documents, images, and videos (00:22:31–00:23:07).
- He introduces “Agentic Mode,” an upcoming July enhancement for reasoning across documents to derive complex answers rather than just extracting values (00:31:01–00:33:18).

### [BRK243] Claw and agent harness in Microsoft Foundry
*Speakers:* Glenn Condron, Amanda Foster, Shawn Henry  
[Session page](https://build.microsoft.com/en-US/sessions/BRK243) · [Video](https://medius.microsoft.com/Embed/video-nc/ce857844-2448-482c-a66b-efa81e214b35)

- Amanda then introduces a new generation called “Autopilot agents” (00:39:46), which act autonomously with their own user identities, allowing them to send messages, manage documents, and perform independent actions traditionally limited to human accounts.

### [BRK246] Foundry IQ: Fuel agents with enterprise knowledge and agentic retrieval
*Speakers:* Pablo Castro, Allison Sparrow  
[Session page](https://build.microsoft.com/en-US/sessions/BRK246) · [Video](https://medius.microsoft.com/Embed/video-nc/ae80fe5d-7c1e-4fc5-ab1c-a37839c0a9bd)

- He transitions to the provisioning process and announces an important milestone—the public preview of the **serverless version of Foundry IQ** (00:09:03).
- This new capability allows developers to create services in 10–20 seconds, with auto-scaling and pay-per-use flexibility.

### [BRK250] Observe and control agents across any framework with open source tools
*Speakers:* Sarah Bird, Sandeep Atluri, Mehrnoosh Sameki, Katelyn Rothney  
[Session page](https://build.microsoft.com/en-US/sessions/BRK250) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/b919f3dd-95e5-41c4-9ea5-7604e8d87df8) · [Video](https://medius.microsoft.com/Embed/video-nc/b919f3dd-95e5-41c4-9ea5-7604e8d87df8)

- Future Frontiers and Responsible Collaboration: In closing, Byrd and Sandeep preview upcoming advancements including continuous evaluations powered by reinforcement-learning attackers that adapt tests based on production performance 00:37:03–00:39:20.

### [BRK252] From observability to ROI for AI agents on any framework
*Speakers:* Vivek Bhadauria, Sebastian Kohlmeier, Filisha Shah  
[Session page](https://build.microsoft.com/en-US/sessions/BRK252) · [Video](https://medius.microsoft.com/Embed/video-nc/bc75ad49-f354-49ee-a449-69cb12bcf5fb)

- Multi-Turn Evaluation and Continuous Improvement: The session continues with announcements of advanced public preview features—multi-turn evaluation and user simulation 00:17:48.
- Demo 2: Agent Optimization at Scale: Vivek takes the stage to showcase “Agent Optimizer,” a new feature designed for iterative, automated optimization of AI agents based on rubrics and datasets 00:21:01.
- The presentation closes with upcoming session invitations and encouragement to explore the Foundry hands-on labs available at Build 00:35:19.

### [BRK260] Build Apps w\/ Local AI for Unmetered Intelligence on every Windows PC
*Speakers:* Jordi Janer, Aditi Narvekar, Anastasiya Tarnouskaya, Tucker Burns  
[Session page](https://build.microsoft.com/en-US/sessions/BRK260) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/04c29fa8-c492-43f5-bb90-6582b474053b) · [Video](https://medius.microsoft.com/Embed/video-nc/04c29fa8-c492-43f5-bb90-6582b474053b)

- The narrative promises announcements, live demos across multiple devices, and focuses on Microsoft's vision of "unmetered intelligence"—running AI directly on PCs instead of relying exclusively on the cloud 00:01:01–00:01:12.
- Code walkthroughs reveal simplified model download, load, and inference routines for developers.
- This leads into a detailed explanation of Windows ML’s general availability and new tooling, notably the Windows ML CLI preview 00:21:28–00:27:00, which optimizes models through conversion, analysis, and benchmarking in one workflow.

### [BRKSP91] Turn foundation models into production AI on Microsoft Foundry
*Speakers:* Vivek Chauhan, Alicia Frame, Jetashree Ravi  
[Session page](https://build.microsoft.com/en-US/sessions/BRKSP91) · [Video](https://medius.microsoft.com/Embed/video-nc/1ce61725-4e6d-40e0-902f-a17d1366824a)

- Demo and Foundry Integration Announcement: The next section presents practical demos of Fireworks tools and the major announcement of its availability on Microsoft Foundry (00:14:42).

### [BRKSP94] Orchestrate special agents with NVIDIA Nemotron models on Foundry
*Speakers:* Joey Conway, AYSEN Ilkbahar, Stephen McCullough  
[Session page](https://build.microsoft.com/en-US/sessions/BRKSP94) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/6c7fb279-6292-41b9-8bf5-5d5b12d9eb25) · [Video](https://medius.microsoft.com/Embed/video-nc/6c7fb279-6292-41b9-8bf5-5d5b12d9eb25)

- Announced recently, Nemotron 3 Ultra integrates advanced training techniques like multi-teacher distillation (00:09:08) and new NVFP4 precision formats for NVIDIA Blackwell architecture, allowing one unified checkpoint for device compatibility.

### [DEM310] Ship code faster with AI-powered NoSQL schema design
*Speakers:* Marko Hotti, Sergiy Smyrnov  
[Session page](https://build.microsoft.com/en-US/sessions/DEM310) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/43d42b09-edf5-442a-8016-5661a369e0f1) · [Video](https://medius.microsoft.com/Embed/video-nc/43d42b09-edf5-442a-8016-5661a369e0f1)

- Marco and Sergei are introduced as the speakers who will discuss how to ship code faster using AI-powered NoSQL schema design.

### [DEM312] Multi-agents in action with 3 AI agents, 3 frameworks, tools & models
*Speakers:* Jan Kalis, Vini Soto  
[Session page](https://build.microsoft.com/en-US/sessions/DEM312) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/d23cefd0-8854-4932-a055-1022d8c5aa15) · [Video](https://medius.microsoft.com/Embed/video-nc/d23cefd0-8854-4932-a055-1022d8c5aa15)

- Introducing Azure Container App Sandboxes: The speakers discuss typical runtime problems—like cold starts, untrusted code execution, and lack of lifecycle control—and introduce Azure Container App Sandboxes as a solution (00:02:28–00:02:56).
- They announce a private preview of this feature, emphasizing its secure, isolated, and stateful infrastructure on demand.
- The presenters close with an invitation to upcoming sessions and demos at Build, thanking the audience for participating and reiterating Microsoft’s mission to make multi-agent orchestration secure, manageable, and developer-friendly.

### [DEM323] Under the hood of Microsoft AI models
*Speakers:* Dave Citron  
[Session page](https://build.microsoft.com/en-US/sessions/DEM323) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/737e6687-341c-48f1-955a-62f5f84e88a1) · [Video](https://medius.microsoft.com/Embed/video-nc/737e6687-341c-48f1-955a-62f5f84e88a1)

- Conclusion and Availability: In closing at 00:16:48, Citron summarizes that Image 2.5, Voice 2, and Transcribe 1.5 are live today on Foundry and Microsoft’s Mai Playground, accessible even through mobile devices, while Thinking 1 is entering private preview through Foundry. "Code 1 Flash" is available in Visual Studio Code.

### [DEM331] Turn APIs, tools, and data into real agent velocity
*Speakers:* Chu Lahlou  
[Session page](https://build.microsoft.com/en-US/sessions/DEM331) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/f08b2f52-65fb-4621-90fd-7813993f93ca) · [Video](https://medius.microsoft.com/Embed/video-nc/f08b2f52-65fb-4621-90fd-7813993f93ca)

- To address these challenges, the concept of “content understanding” is introduced as a method to transform messy, multimodal inputs into clean, structured outputs (00:01:47–00:02:13), formatted as Markdown or JSON containing agent-ready inputs.
- The video closes by inviting viewers to explore full demo code on GitHub and attend a related breakout session on upcoming advancements like Generative Tech Mode and Foundry integration (00:21:19–00:21:47).

### [DEM333] How Foundry integrates with open-source frameworks and tools
*Speakers:* Nagkumar Arkalgud, Facundo Santiago  
[Session page](https://build.microsoft.com/en-US/sessions/DEM333) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/60554504-db91-4d72-a3de-4f1c346b7ceb) · [Video](https://medius.microsoft.com/Embed/video-nc/60554504-db91-4d72-a3de-4f1c346b7ceb)

- Introducing Skills and Web Interaction: The conversation shifts to enhancing agent intelligence using “skills” — reusable playbooks defining sequences of actions like inbox triage (00:04:38).
- Demonstrations reveal trace replays showing user input, tool actions, and token costs across the workflow.

### [DEM340] Build work-ready agents with Foundry + Work IQ, govern with Agent 365
*Speakers:* Srikumar (Sri) Nair  
[Session page](https://build.microsoft.com/en-US/sessions/DEM340) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/4ce5f64d-3565-4d14-8010-32ad80dc7524) · [Video](https://medius.microsoft.com/Embed/video-nc/4ce5f64d-3565-4d14-8010-32ad80dc7524)

- He announces general availability targeting mid-June 00:03:11, promising full security compliance so agents only see appropriate data per identity permissions.

### [DEM341] Any agent, any cloud: Standardized tracing with Foundry+OpenTelemetry
*Speakers:* Nagkumar Arkalgud, Hanchi Wang  
[Session page](https://build.microsoft.com/en-US/sessions/DEM341) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/f1e85c0c-4927-4179-bf56-f6ec097af7dc) · [Video](https://medius.microsoft.com/Embed/video-nc/f1e85c0c-4927-4179-bf56-f6ec097af7dc)

- This establishes how Foundry’s observability reveals agent reasoning and behavior step by step.

### [DEM345] From prompt to app, build AI powered apps on Windows
*Speakers:* Nikola Metulev, Lei Xu  
[Session page](https://build.microsoft.com/en-US/sessions/DEM345) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/851eb058-a594-4193-8437-6010e4400b02) · [Video](https://medius.microsoft.com/Embed/video-nc/851eb058-a594-4193-8437-6010e4400b02)

- Optimizing AI Models with WinML: Around 00:09:38, the presenters unveil a newly released tool — WinML CLI.

### [DEM361] Understand and fix Agent Framework apps with observability and evals
*Speakers:* Jim Bennett  
[Session page](https://build.microsoft.com/en-US/sessions/DEM361) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/65ab30d5-8261-422e-8be7-119ad843b8ee) · [Video](https://medius.microsoft.com/Embed/video-nc/65ab30d5-8261-422e-8be7-119ad843b8ee)

- Through Phoenix, he shows how evals produce simple deterministic scores (supported/unsupported) and reveals that his agent is only correct around half the time.

### [DEM362-R1] Building a Multi-Agent Workflow in Microsoft Fabric
*Speakers:* Alexander Wachtel  
[Session page](https://build.microsoft.com/en-US/sessions/DEM362-R1) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/d48b1a04-b191-438e-963b-2b3b03577cb6) · [Video](https://medius.microsoft.com/Embed/video-nc/d48b1a04-b191-438e-963b-2b3b03577cb6)

- Agent SDK, Evaluation, and Governance: Alex moves deeper into technical territory by introducing the Data Agent SDK 00:19:45–00:21:01.

### [DEM368-R1] Data Science & Machine Learning with Microsoft Fabric
*Speakers:* Prashant G Bhoyar  
[Session page](https://build.microsoft.com/en-US/sessions/DEM368-R1) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/4924e612-6605-49b7-9f01-7b9fab96e6e7) · [Video](https://medius.microsoft.com/Embed/video-nc/4924e612-6605-49b7-9f01-7b9fab96e6e7)

- Introducing Fabric Data Agents: The next section shifts focus to Fabric’s data agent capabilities—a generative AI-powered feature that lets everyday users query their data intuitively without complex SQL writing (00:14:49).

### [DEMSP380] Build automated agents using optimized AI Foundry models on Snapdragon
*Speakers:* Darren Oberst, Meghana Rao, Morris Novello  
[Session page](https://build.microsoft.com/en-US/sessions/DEMSP380) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/5598fc68-e815-4c2e-b5fc-b9bd4ad90c22) · [Video](https://medius.microsoft.com/Embed/video-nc/5598fc68-e815-4c2e-b5fc-b9bd4ad90c22)

- Introduction and Motivation: At the start of the session 00:00:01–00:00:13, the presenters introduce the goal of demonstrating how to build automated AI agents using optimized models available in Microsoft Foundry for Snapdragon PCs.

### [DEMSP383] Move AI workflows from test to production on Microsoft Foundry
*Speakers:* Vignesh Sridhar  
[Session page](https://build.microsoft.com/en-US/sessions/DEMSP383) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/2d0d8c96-5737-41f7-8a54-7be68b88101f) · [Video](https://medius.microsoft.com/Embed/video-nc/2d0d8c96-5737-41f7-8a54-7be68b88101f)

- The session ends with Manesh expressing gratitude for the presentation and sharing a brief announcement about the next upcoming session, encouraging participants to stay or have a great day 00:13:58–00:14:26.

### [DEMSP388] Ship faster with Claude Code and Cowork in Microsoft Foundry
*Speakers:* Caroline Matthews, Ryan Whitehead  
[Session page](https://build.microsoft.com/en-US/sessions/DEMSP388) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/46e9fb81-4bb9-4d1c-a5e4-ca32bd1bb8ff) · [Video](https://medius.microsoft.com/Embed/video-nc/46e9fb81-4bb9-4d1c-a5e4-ca32bd1bb8ff)

- Caroline then announces the recent model release, Opus 4.8, describing it as Anthropic’s most advanced Frontier Intelligence offering ideal for accuracy-critical, long-horizon tasks 00:02:12.
- She introduces “dynamic workflows,” a new feature in Opus 4.8 enabling modular, sub-agent collaboration.
- First Frontier – Autonomy and Safety: Caroline discusses reducing human bottlenecks by introducing auto mode, a new classifier-based safety layer between model requests and execution permissions 00:06:35.

### [DEMSP390] Create multimodal AI agents with persistent memory
*Speakers:* Edo Segal  
[Session page](https://build.microsoft.com/en-US/sessions/DEMSP390) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/9228bcee-53b2-4fd0-b6a7-83ca65070cfd) · [Video](https://medius.microsoft.com/Embed/video-nc/9228bcee-53b2-4fd0-b6a7-83ca65070cfd)

- Later, Microsoft’s representative joins to announce Napster’s public preview as a native Azure offering 00:04:38–00:05:05.

### [DEMSP393] Orchestrate omnichannel AI agents with Foundry and Twilio
*Speakers:* Rachel Baskin  
[Session page](https://build.microsoft.com/en-US/sessions/DEMSP393) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/c1269a04-04cc-4d61-b461-41f96f288bac) · [Video](https://medius.microsoft.com/Embed/video-nc/c1269a04-04cc-4d61-b461-41f96f288bac)

- To solve scalability and security isolation issues, Microsoft introduced “hosted agents,” a new compute model built for persistent, secure, stateful sessions 00:05:22.

### [KEY01] Microsoft Build opening keynote
*Speakers:* Satya Nadella  
[Session page](https://build.microsoft.com/en-US/sessions/KEY01) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/9b6fd85d-e64f-46a4-b8b2-23811087192f) · [Video](https://medius.microsoft.com/Embed/video-nc/9b6fd85d-e64f-46a4-b8b2-23811087192f)

- Developers are introduced to the Surface RTX Spark Dev Box at 00:08:06, a machine delivering petaflop-level AI compute designed specifically for software creation.
- He unveils innovations like the AMD MI300 and the custom ARM-based Cobalt CPUs and networks designed for the dominant AI workloads: training, inference, and agent runtime.
- Stevie Bathiche and team reveal this as the platform for new "agent-first" computing—an ecosystem that connects specialized devices through Azure.
- The keynote concludes with the unveiling of the Majorana 2 quantum chip at 02:19:04, achieving breakthrough reliability and density for the coming quantum era.

### [LIVE142] Student to Startup
*Speakers:* Alycea Adams, Tom Davis  
[Session page](https://build.microsoft.com/en-US/sessions/LIVE142) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/b2a624c7-5cb0-4a3d-b252-274a14cef87e) · [Video](https://medius.microsoft.com/Embed/video-nc/b2a624c7-5cb0-4a3d-b252-274a14cef87e)

- User Insights and Future Vision: In the final section, 00:09:09–00:13:13, Alicia reveals that her expected audience of young individual users evolved into mothers seeking solutions for their daughters’ hair.

### [LIVE143] What’s New in Azure Data: HorizonDB and Rayfin
*Speakers:* Charles Feddersen, Sachin Patney, Nikisha Reyes-Grange  
[Session page](https://build.microsoft.com/en-US/sessions/LIVE143) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/e6e02047-ba96-4845-9f56-11be582215ec) · [Video](https://medius.microsoft.com/Embed/video-nc/e6e02047-ba96-4845-9f56-11be582215ec)

- Charles, the Director of Program Management for Postgres and MySQL on Azure, and Sachin, the General Manager of App Development for Azure Data, join to share key data announcements made at Build.
- Azure Horizon DB Announcement: Charles explains that Azure Horizon DB is a newly announced Postgres-based database service designed for developers and enterprises 00:00:45.
- Microsoft is among the largest contributors to the upstream Postgres project, modifying roughly 8% of the codebase in the upcoming version 19 00:09:03.

### [LIVE159] Behind the Scenes: Accelerating the AI Agent DevOps Lifecycle with End-to-End Observability
*Speakers:* Vivek Bhadauria, Nitya Narasimhan, Filisha Shah  
[Session page](https://build.microsoft.com/en-US/sessions/LIVE159) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/47bd4df9-ea64-49d9-bd10-d4e2f5baefcc) · [Video](https://medius.microsoft.com/Embed/video-nc/47bd4df9-ea64-49d9-bd10-d4e2f5baefcc)

- The panel notes that “Agent Optimizer” is currently in gated preview and will soon be available in public preview 00:05:49–00:05:57, inviting developers to try it and provide feedback.

### [LIVE163] Toolboxes in Foundry: Build, Search and Govern Your Tools
*Speakers:* Atul Aggarwal, Seth Juarez, Linda Li  
[Session page](https://build.microsoft.com/en-US/sessions/LIVE163) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/ad613b19-51cf-4c92-a4c5-cae4670df3ae) · [Video](https://medius.microsoft.com/Embed/video-nc/ad613b19-51cf-4c92-a4c5-cae4670df3ae)

- Linda announces that Toolbox is currently in public preview and will achieve general availability later this month 00:13:17–00:13:34.

### [LIVE171] The Three IQs: Ground Your Agents in Knowledge, Data, and Work
*Speakers:* Ayca Bas, Marco Casalaina  
[Session page](https://build.microsoft.com/en-US/sessions/LIVE171) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/eaaffcc3-d8a7-47ab-a42c-d84a91d007e7) · [Video](https://medius.microsoft.com/Embed/video-nc/eaaffcc3-d8a7-47ab-a42c-d84a91d007e7)

- Preventing Context Redundancy and Introducing Agent Templates: The next section discusses how IQs help reduce “context rot,” meaning developers no longer need to overload agents with excessive contextual data (00:05:00–00:05:17).

### [LIVESP122] Intel quick take: Live from Microsoft Build
*Speakers:* Bryan Hiestand  
[Session page](https://build.microsoft.com/en-US/sessions/LIVESP122) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/ac4e728e-13e3-415e-bae4-1e118bc96b6a) · [Video](https://medius.microsoft.com/Embed/video-nc/ac4e728e-13e3-415e-bae4-1e118bc96b6a)

- The host enthusiastically announces a special guest from NVIDIA, Steven, who will be sharing details about innovative projects his team has been developing.
- Highlighting the Technological Innovations: The host responds with enthusiasm about the upcoming demonstration, emphasizing the value of seeing technology in action 00:00:57.

### [LIVESP123] NVIDIA quick take: Live from Microsoft Build
*Speakers:* Stephen McCullough  
[Session page](https://build.microsoft.com/en-US/sessions/LIVESP123) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/c4d84be5-ddcd-494b-9489-a35eb76b26ed) · [Video](https://medius.microsoft.com/Embed/video-nc/c4d84be5-ddcd-494b-9489-a35eb76b26ed)

- The host enthusiastically announces a special guest from NVIDIA, Steven, who will be sharing details about innovative projects his team has been developing.
- Highlighting the Technological Innovations: The host responds with enthusiasm about the upcoming demonstration, emphasizing the value of seeing technology in action 00:00:57.

### [LIVESP129] Organizational intelligence in action — with Anthropic
*Speakers:* Max Kirby  
[Session page](https://build.microsoft.com/en-US/sessions/LIVESP129) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/8a1f6f67-1328-4be4-8a17-c0fff1c551ce) · [Video](https://medius.microsoft.com/Embed/video-nc/8a1f6f67-1328-4be4-8a17-c0fff1c551ce)

- This section transitions into discussions about Microsoft’s new “IQ” announcements—Work IQ, Foundry IQ, Fabric IQ, and Web IQ—which enable reasoning across multiple domains 00:02:10–00:02:21.

### [OD805] AI Building Blocks for .NET: Add intelligence to your C# apps
*Speakers:* —  
[Session page](https://build.microsoft.com/en-US/sessions/OD805) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/77f11a3c-9f3d-4ac6-9ea4-fef86c97f73a) · [Video](https://medius.microsoft.com/Embed/video-nc/77f11a3c-9f3d-4ac6-9ea4-fef86c97f73a)

- He introduces Aspire traces to monitor service interactions and sets the context for the upcoming deep dive into the .NET AI architecture.
- Integrating External Tools with MCP: Bruno transitions to introducing the Model Context Protocol (MCP), a standard enabling AI applications to access external tools and APIs 00:23:01.

### [OD811] Powering the next AI frontier with a unified data platform
*Speakers:* Amir Netz, Eren Orbey  
[Session page](https://build.microsoft.com/en-US/sessions/OD811) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/4b833a99-c06b-4edf-b6a8-5063fc488c92) · [Video](https://medius.microsoft.com/Embed/video-nc/4b833a99-c06b-4edf-b6a8-5063fc488c92)

- By 00:07:09, he announces new data connectors for SAP, Oracle, SharePoint, OneDrive, and previews for AWS Glue and Azure Monitor, reinforcing a “zero-ETL” approach for complete data unification.
- Performance, Agent Skills, and AI Functions: Starting at 00:08:08, Amir unveils GPU-accelerated query performance in the Fabric Data Warehouse, achieving up to 8x to 100x improvements under concurrent workloads — a breakthrough showcased in multiple demos.
- This naturally leads to the announcement of the general availability of “Planning in Fabric” at 00:22:00.
- Finally, the narration transitions at 00:33:05 to “operations agents,” now generally available.

### [ODSP909] Take AI agents from prototype to production with OpenTelemetry
*Speakers:* Harry Kimpel  
[Session page](https://build.microsoft.com/en-US/sessions/ODSP909) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/05becd32-00b0-410e-adb0-4dc892dbde19) · [Video](https://medius.microsoft.com/Embed/video-nc/05becd32-00b0-410e-adb0-4dc892dbde19)

- Built-in telemetry reveals “what” happened but not “why,” prompting the addition of custom spans and metrics for enriched context (00:07:55).

### [ODSP922] Develop a conversational search experience without rebuilding your app
*Speakers:* Greg Crist  
[Session page](https://build.microsoft.com/en-US/sessions/ODSP922) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/107cd1bc-d7fd-428c-8a8c-fa58870c3a9a) · [Video](https://medius.microsoft.com/Embed/video-nc/107cd1bc-d7fd-428c-8a8c-fa58870c3a9a)

- Overview of Elastic Solutions: Jonathan Simon begins his portion at 00:02:04 by introducing himself and the structure of his presentation, which includes an overview, demo, and architectural walkthrough.
- He then officially announces the general availability of Elastic Agent Builder at 00:04:55, marking its transition from technical preview to production-ready status.

---

## AI Infrastructure

_Azure AI infrastructure — Maia/Cobalt silicon, Manifold, Context Cache, prompt caching, inference optimization, containers_

### [BRK206-R1] Your agent, anywhere: MultiClient, MultiDevice with GitHub Copilot SDK
*Speakers:* Patrick Nikoletich, Steve Sanderson  
[Session page](https://build.microsoft.com/en-US/sessions/BRK206-R1) · [Video](https://medius.microsoft.com/Embed/video-nc/77be1034-59af-4388-bdb6-37a99f2acae7)

- Patrick outlines that they will discuss how to build and deploy with the SDK, touch on upcoming features, and share follow-up resources.
- He announces that the GitHub Copilot SDK has reached its General Availability milestone at version 1.0 (00:00:32–00:00:38), marking the end of a year-long journey from technical preview to official release.
- This shared “harness” ensures that experiences remain consistent across GitHub and Microsoft’s broader ecosystem, introducing a uniform Copilot feel across different products.

### [BRK226] Inside Azure innovations with Mark Russinovich
*Speakers:* Mark Russinovich, Darby Kosten  
[Session page](https://build.microsoft.com/en-US/sessions/BRK226) · [Video](https://medius.microsoft.com/Embed/video-nc/e959dc6a-bb39-46a9-84c5-b2620675b658)

- Azure Boost is then introduced as a central innovation—it uses offload cards to move data paths for storage and networking from CPUs to dedicated DPUs, boosting throughput significantly.

### [BRK234] Shipping custom models at scale from fine-tuning to inference
*Speakers:* Rob Ferguson, Daniel Han, Mark Saroufin  
[Session page](https://build.microsoft.com/en-US/sessions/BRK234) · [Video](https://medius.microsoft.com/Embed/video-nc/990ffabd-eceb-4850-96a4-e40c4c2e7df8)

- Rob describes how elegant RL training recipes differ dramatically from actual infrastructure needs, emphasizing that math abstractions often reveal themselves as large GPU production costs.

### [BRK235] Local models, developer control, and the future of AI runtimes
*Speakers:* Michael Chiang, Parth Sareen  
[Session page](https://build.microsoft.com/en-US/sessions/BRK235) · [Video](https://medius.microsoft.com/Embed/video-nc/0f29bea1-6955-4ec3-8c51-5a80b47dcf7b)

- He notes partnerships with major model and hardware providers and announces that DeepMind’s new Jemma 4-12B unified model is already hosted and available on the O Llama platform (00:02:06–00:02:18).
- Upcoming hardware trends toward unified memory from NVIDIA, AMD, and Microsoft will further improve performance and model capacity (00:16:00–00:17:15).

### [BRK244] Agent supervision is the new senior engineering skill
*Speakers:* swyx (Shawn Wang)  
[Session page](https://build.microsoft.com/en-US/sessions/BRK244) · [Video](https://medius.microsoft.com/Embed/video-nc/c8e844ff-d07c-427f-9168-2a7d84ac4acf)

- He then transitions to upcoming AI research priorities (00:30:29): real-time responsiveness, memory and continual learning, and interactive micro-batching aimed at human-machine “mind melds.” This vision includes video generation driven by orchestrating agents and the rise of world models capable of predicting user preferences and intentions.

### [BRK262] Building Agents You Can Trust on Windows
*Speakers:* Kirupa Chinnathambi, Patrick Nikoletich, Stuart Schaefer  
[Session page](https://build.microsoft.com/en-US/sessions/BRK262) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/ceeb5203-d352-4d45-8be6-9db57724f003) · [Video](https://medius.microsoft.com/Embed/video-nc/ceeb5203-d352-4d45-8be6-9db57724f003)

- He reveals how users can toggle protection, customize network filters, and observe sandbox restrictions while maintaining developer flexibility across CLI, SDK, and integrated apps.
- She introduces the upcoming integration with Agent 365 built over MXC, which supports enterprise-grade protections through Defender, Entra, and Intune 00:27:27–00:27:50.

### [BRKSP90] Stop routing docstrings to 70B models with on-device AI on Snapdragon
*Speakers:* Alberto Martinez, Morris Novello  
[Session page](https://build.microsoft.com/en-US/sessions/BRKSP90) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/77723cdd-4ddd-4ede-8582-8ec8771be197) · [Video](https://medius.microsoft.com/Embed/video-nc/77723cdd-4ddd-4ede-8582-8ec8771be197)

- Introducing himself as the head of software strategy for Qualcomm’s compute business, he explains that his talk will be somewhat improvised, fitting for the creative “improv” venue (00:00:23).

### [DEM346] WSL improvements and the new Containers CLI and APIs
*Speakers:* Craig Loewen, Pooja Trivedi  
[Session page](https://build.microsoft.com/en-US/sessions/DEM346) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/4025f713-c725-4c66-a946-2ab72f10c1ad) · [Video](https://medius.microsoft.com/Embed/video-nc/4025f713-c725-4c66-a946-2ab72f10c1ad)

- Introduction and Key Announcements: The session begins with Pooja Trivedi and Craig introducing themselves and unveiling a new capability known as WSL Containers (00:00:20).
- CLI Demonstration and Basic Container Operations: Pooja demonstrates how WSL Containers can be accessed and managed using a new tool called WSLC, available after a simple WSL update (00:01:33).
- Before closing, she mentions additional updates including Azure Linux 4.0’s availability and its upcoming inclusion as a WSL distribution (00:21:52).

### [DEMSP381] Scale agentic AI cost‑efficiently on Azure with Arm Cobalt VMs
*Speakers:* Gova Babu, Pranay Bakre, Sameer Nori  
[Session page](https://build.microsoft.com/en-US/sessions/DEMSP381) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/2796f78a-ca86-49c1-98cc-ba57308ea186) · [Video](https://medius.microsoft.com/Embed/video-nc/2796f78a-ca86-49c1-98cc-ba57308ea186)

- Goa announces that Cobalt 200 VMs, built on 3nm ARM architecture and optimized for Microsoft workloads, now ship with Azure Boost and achieve around 50% better per-core performance compared to the previous generation (00:03:35–00:04:12).
- The VMs are now available in preview across eight regions, with more expansion planned upon general availability (00:06:33–00:06:46).
- He highlights upcoming hands-on lab sessions and invites participants to explore ARM Cloud Migration resources, which assist in transitioning workloads to ARM64 with performance analysis and engineering support (00:16:02–00:16:38).

### [DEMSP384] Profile and optimize agentic AI on Windows
*Speakers:* Freddy Chiu, Vasanth Tovinkere  
[Session page](https://build.microsoft.com/en-US/sessions/DEMSP384) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/181d1850-faaf-4f02-b3ce-293fa47f1b5f) · [Video](https://medius.microsoft.com/Embed/video-nc/181d1850-faaf-4f02-b3ce-293fa47f1b5f)

- The segue to profiling is introduced by posing the challenge of measuring performance to optimize such multi-step, multimodal workflows 00:02:55–00:03:06.
- The results reveal trade-offs between speed and power consumption, allowing informed workload deployment strategies.

### [DEMSP386] Develop faster on Windows with AI playbooks and local agents
*Speakers:* Adrian Macias  
[Session page](https://build.microsoft.com/en-US/sessions/DEMSP386) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/3e9502fa-d5ca-49a3-a3bb-69d4be31d73f) · [Video](https://medius.microsoft.com/Embed/video-nc/3e9502fa-d5ca-49a3-a3bb-69d4be31d73f)

- The speaker highlights developer enthusiasm—mentioning community projects and cross-vendor contributions—and reveals the upcoming “Halo box,” a headless PC appliance designed for continuous AI agent operation and background automation tasks 00:23:26–00:24:22.
- Conclusion and Call to Action: The session closes with an invitation to explore AMD’s Developer Portal (00:24:26–00:25:26), where visitors will find announcements on Halo, Lemonade updates, and Playbook workshops.

### [DEMSP387] Secure agent workflows in GitHub Copilot with NVIDIA OpenShell
*Speakers:* Ali Golshan, Alex Watson  
[Session page](https://build.microsoft.com/en-US/sessions/DEMSP387) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/b73f26f9-8342-4119-b417-82d0136435b9) · [Video](https://medius.microsoft.com/Embed/video-nc/b73f26f9-8342-4119-b417-82d0136435b9)

- The speakers invite community testing and contributions, noting that the alpha version debuted at GTC in March and will advance to beta soon.

### [LIVE109] What’s real, ready, and next for developers with Scott Guthrie
*Speakers:* Scott Guthrie, Seth Juarez  
[Session page](https://build.microsoft.com/en-US/sessions/LIVE109) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/66e36077-6ee0-4e48-a7e4-c206c235379b) · [Video](https://medius.microsoft.com/Embed/video-nc/66e36077-6ee0-4e48-a7e4-c206c235379b)

- Fabric IQ—now generally available—connects semantic data directly to Copilot in Microsoft 365 for more intelligent organizational insights (00:09:40–00:10:11).
- As AI agents and automated systems introduce millions of requests per second, the architecture must evolve beyond conventional relational designs to globally replicated systems capable of ultra-low latency.
- The video concludes as Seth thanks Guthrie, who confirms that the upcoming AI-driven transformation will be vast and exhilarating for developers and technologists alike (00:14:16–00:14:22).

### [LIVE148] How Xoople Scales Python for AI using Anyscale on Azure
*Speakers:* Milos Colic, Nate Waters  
[Session page](https://build.microsoft.com/en-US/sessions/LIVE148) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/20919845-b4f7-4ac7-ad3f-4a954711c3b5) · [Video](https://medius.microsoft.com/Embed/video-nc/20919845-b4f7-4ac7-ad3f-4a954711c3b5)

- Technical Implementation with AnyScale on Azure: Nate transitions to discuss Microsoft’s new announcement—“AnyScale on Azure” (00:02:56).
- The conversation concludes with Nate thanking Milos for joining Microsoft Build and encouraging viewers to explore AnyScale on Azure, which is now available in public preview (00:14:06).

### [LIVE158] How Microsoft AI builds coding models optimized for GitHub Copilot
*Speakers:* Pierce Boggan, Pengcheng He, Seth Juarez, Yang Liu  
[Session page](https://build.microsoft.com/en-US/sessions/LIVE158) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/0a23b038-c73a-4b01-901d-9098e033af9a) · [Video](https://medius.microsoft.com/Embed/video-nc/0a23b038-c73a-4b01-901d-9098e033af9a)

- Users are encouraged to provide feedback to refine future “powerful beasts.” The host concludes enthusiastically, thanking the team and urging developers to stay tuned for upcoming iterations, applauding the innovation that merges efficiency, intelligence, and practical coding application.

### [LIVE165] Is DOOM a Tensor?
*Speakers:* Burke Holland, Anthony Shaw  
[Session page](https://build.microsoft.com/en-US/sessions/LIVE165) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/520dcf59-8b05-4f90-aee1-42ae648865ab) · [Video](https://medius.microsoft.com/Embed/video-nc/520dcf59-8b05-4f90-aee1-42ae648865ab)

- Anthony Shaw is introduced as a technical advisor and former Python advocate at Microsoft, having contributed to Python-related work for several years.
- Despite performance challenges, this playful experiment becomes part of Microsoft Build 2026’s announcements, showing “Doom runs in Excel” in a retro AI-generated promotion.

### [LIVE172] Build and ship faster with a developer-optimized Windows experience
*Speakers:* Nikola Metulev, Beth Pan, Aditya Ramnathkar  
[Session page](https://build.microsoft.com/en-US/sessions/LIVE172) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/8eb66ee9-b869-4e25-a1e3-d19c18f30d2b) · [Video](https://medius.microsoft.com/Embed/video-nc/8eb66ee9-b869-4e25-a1e3-d19c18f30d2b)

- Following this, Nicola introduces “WSL Containers” — a new capability that enables containerized development natively on Windows via the WSLC binary 00:06:00–00:06:39.
- AI Hardware and Closing Reflections: The presentation closes with Aditya introducing the new Surface RTX Spark Dev Box 00:14:22, a purpose-built developer machine with NVIDIA RTX Spark GPU configured for local AI computation featuring up to 1 petaflop of performance and 128 GB of unified memory.

### [OD828] Latest Cobalt VMs and Azure Boost enhancements​
*Speakers:* Amar Dhamdhere, Niko Pamboukas  
[Session page](https://build.microsoft.com/en-US/sessions/OD828) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/928b0d8e-af20-4b87-a5b6-8becc44e2911) · [Video](https://medius.microsoft.com/Embed/video-nc/928b0d8e-af20-4b87-a5b6-8becc44e2911)

- Introduction and Overview of Azure Cobalt: The video begins with Amar Dhamdhere introducing himself as a Project Manager from the Azure Compute VM Sizes Team and sets the context by describing Azure’s commitment to optimized virtual machine (VM) performance (00:00:07).
- Benchmarks reveal consistent gains across industry-standard, Microsoft-internal, and real product workloads—all confirming per-core performance improvements.
- Intel, AMD VM Announcements and Azure Compute Security Innovations: The final segments feature Amar detailing new Intel and AMD general compute VMs powered by Azure Boost and next-gen CPUs (00:24:35).

### [ODSP900] Performance tuning on Cobalt with Arm Performix​
*Speakers:* David Haikney  
[Session page](https://build.microsoft.com/en-US/sessions/ODSP900) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/96f9277a-f0b3-4e0c-8d91-55c4b9785084) · [Video](https://medius.microsoft.com/Embed/video-nc/96f9277a-f0b3-4e0c-8d91-55c4b9785084)

- Basic Concepts and Setup: When introducing the Performix UI (00:02:07), David explains that users can work through the interface or the command line.

---

## Models

_Frontier and open models — MAI family, GPT-5.x, Claude/Anthropic, Llama, Mistral, Phi, Aurora geospatial, Image 2.5_

### [BRK200] Why your AI code doesn’t ship: Closing the gap to production
*Speakers:* Mario Rodriguez, Evan Boyle  
[Session page](https://build.microsoft.com/en-US/sessions/BRK200) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/a6e942b5-ceab-40f1-9a69-03390a58d306) · [Video](https://medius.microsoft.com/Embed/video-nc/a6e942b5-ceab-40f1-9a69-03390a58d306)

- Finally, Evan unveils “Agent Merge,” which autonomously manages pull requests, reacts to feedback, resolves conflicts, and merges code once tests pass (00:26:07).

### [BRK203] From CLI to PR: Automating the path to merged code
*Speakers:* Evan Boyle, Cassidy Williams, Katie Liu  
[Session page](https://build.microsoft.com/en-US/sessions/BRK203) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/b2b9417e-2b22-4732-aaac-24df66a625f7) · [Video](https://medius.microsoft.com/Embed/video-nc/b2b9417e-2b22-4732-aaac-24df66a625f7)

- AI Tools and the Power of the CLI: After introducing the broader landscape, Cassidy highlights the ascendancy of AI development tools, situating GitHub Copilot as central to this productivity transformation 00:02:01.
- The “experimental” mode is portrayed as a space for early adopters to test upcoming features such as voice mode, which enables spoken interaction directly in the terminal 00:10:50.
- Cassidy also announces the CLI’s integration with JetBrains IDEs, allowing developers to harness Copilot agents without leaving their editors 00:14:24.
- The GitHub Copilot SDK—built on top of the CLI—is introduced as a foundation for creating custom agent-driven applications across browsers, office software, or chat systems.
- They invite viewers to explore further through GitHub’s free “Copilot CLI for Beginners” course and continue experimenting with new features 00:46:38.

### [DEM303] Late to agentic coding? Don’t panic, build.
*Speakers:* Cassidy Williams, Martin Woodward  
[Session page](https://build.microsoft.com/en-US/sessions/DEM303) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/4c6da11e-f9a7-4141-b2ba-ffec4bfeb86e) · [Video](https://medius.microsoft.com/Embed/video-nc/4c6da11e-f9a7-4141-b2ba-ffec4bfeb86e)

- A quick survey of the audience reveals how many are using GitHub Copilot in different environments such as VS Code, Visual Studio, command line, and the recently announced GitHub app 00:01:20–00:01:40.
- They introduce “Rubber Duck,” a validation step where a second model reviews a plan for logic gaps, demonstrating measurable improvements from multi-model collaboration 00:19:05.
- Closing Thoughts and Call to Action:  
As the session closes, both presenters encourage the audience to continue experimenting with the tools introduced and visit the developer lab areas to collaborate further 00:25:46.

### [DEM315] Embracing frontier R&D with Microsoft Discovery
*Speakers:* John Link, Viktor Veis  
[Session page](https://build.microsoft.com/en-US/sessions/DEM315) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/fdbf653e-2bbd-4ef5-bcdc-d3ff526ebd98) · [Video](https://medius.microsoft.com/Embed/video-nc/fdbf653e-2bbd-4ef5-bcdc-d3ff526ebd98)

- In November 2023, new models like GPT-4.5 and GPT-5.2 introduced advanced AI agency, crossing the threshold where systems could autonomously generate entire solutions—a transformation John predicts is now coming to scientific discovery 00:02:17–00:02:48.
- Introducing Microsoft Discovery and the New App: John explains that Microsoft Discovery enables AI-driven scientific processes at scale, where thousands or even millions of hypotheses can be explored in parallel 00:04:23–00:04:45.
- He recaps prior milestones, noting its introduction at Build as a private preview and its current general availability 00:04:50–00:04:54.

### [DEM350] GitHub Agentic Workflows: Automation That Actually Reads the Room
*Speakers:* Ari LiVigni, Alejandro Menocal  
[Session page](https://build.microsoft.com/en-US/sessions/DEM350) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/ce603017-0583-4aa8-85a6-a7fb79aaa496) · [Video](https://medius.microsoft.com/Embed/video-nc/ce603017-0583-4aa8-85a6-a7fb79aaa496)

- They introduce their discussion topic—GitHub Agentic Workflows—highlighting how automation powered by AI can dynamically "read the room" and adapt processes intelligently 00:00:22.
- Alejandro highlights the ecosystem’s flexibility and mentions the upcoming public preview release planned for the following week, inviting participants to experiment through GitHub’s website and use a new skills exercise to explore workflow capabilities firsthand 00:01:58.

### [DEM360] Discovering Power App Data with M365 Copilot using MCP
*Speakers:* Christine Flora  
[Session page](https://build.microsoft.com/en-US/sessions/DEM360) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/47a31e54-7ea0-4b32-be8e-f7c6400735e6) · [Video](https://medius.microsoft.com/Embed/video-nc/47a31e54-7ea0-4b32-be8e-f7c6400735e6)

- The agenda includes an overview of Power Apps, a live demo building a custom MCP tool with Visual Studio Code and AI assistance, and guidance on prerequisites and setup as the feature enters public preview 00:01:31.
- Christine showcases two advanced UI extensions: an equipment work order dashboard and a timeline visualization for upcoming and overdue maintenance 00:11:28–00:13:32.

### [DEMSP394] Scale enterprise .NET apps with AI‑assisted cross‑platform workflows
*Speakers:* Sam Basu, Colin Whitlatch  
[Session page](https://build.microsoft.com/en-US/sessions/DEMSP394) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/90f6fe71-8cba-465f-b53c-a3ed30e154c6) · [Video](https://medius.microsoft.com/Embed/video-nc/90f6fe71-8cba-465f-b53c-a3ed30e154c6)

- The speakers position the talk as an exploration of how developer tooling is evolving to support agentic, AI-enhanced workflows in real-world applications, setting the tone for multiple announcements during the session.
- Introducing Uno Platform Studio and Tooling: The speakers then present Uno Platform Studio as a suite of AI and design tools for modern .NET development (00:03:16–00:04:55).
- This segment emphasizes context-driven AI, ensuring that generated code aligns with project documentation and user interaction patterns—what they call “AI with eyes and hands.”

Uno Platform Studio 3.0 Announced and Demoed: A major announcement follows—the launch of Uno Platform Studio 3.0 (00:05:08–00:09:00).

### [LIVE101] Scott and Mark learn to Vibe Check
*Speakers:* Scott Hanselman, Mark Russinovich  
[Session page](https://build.microsoft.com/en-US/sessions/LIVE101) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/df6b109e-848b-4a7a-b791-fcd1e8029278) · [Video](https://medius.microsoft.com/Embed/video-nc/df6b109e-848b-4a7a-b791-fcd1e8029278)

- Sanderson unveils “Vibe OS,” described as the world’s first “hallucinated operating system.” Demonstrating live, he boots a lightweight virtual disk file and launches familiar applications such as Notepad and Calculator.
- Through animated queries and “tables,” she reveals that what seems like traditional JavaScript-driven logic is entirely composed of CSS selectors, variables, and sibling indices.

### [LIVE110] Backing the future of innovation
*Speakers:* The Chainsmokers, Charles Lamanna  
[Session page](https://build.microsoft.com/en-US/sessions/LIVE110) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/b149b982-e4e6-475e-8a2d-8c9391b83ab7) · [Video](https://medius.microsoft.com/Embed/video-nc/b149b982-e4e6-475e-8a2d-8c9391b83ab7)

- The group discusses integrating AI into existing workflows—rather than forcing new tool adoption—and applauds the growing movement to bring AI into spaces people already work.

### [LIVE114] Scott and Mark learn to Vibe Check with Cassidy Williams
*Speakers:* Scott Hanselman, Cassidy Williams  
[Session page](https://build.microsoft.com/en-US/sessions/LIVE114) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/aabe7791-a560-45b5-8c66-f6f12a88a9c1) · [Video](https://medius.microsoft.com/Embed/video-nc/aabe7791-a560-45b5-8c66-f6f12a88a9c1)

- Initially, it seems to be a legitimate in-browser SQLite interface, but Cassidy soon reveals the twist: there is no actual database or query engine—everything is powered purely by CSS 00:02:15.
- The session wraps up with thanks to sponsors and an announcement for more quirky and “cursed” coding projects coming after the break 00:11:41.

### [LIVE144] Behind the Keynote: How Windows Made OpenClaw Work in the Keynote Demo
*Speakers:* Monica Cisneros, Scott Hanselman  
[Session page](https://build.microsoft.com/en-US/sessions/LIVE144) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/710e231b-0fbe-47fb-8681-ad4344165d34) · [Video](https://medius.microsoft.com/Embed/video-nc/710e231b-0fbe-47fb-8681-ad4344165d34)

- Introduction and Collaboration Story: The video begins with Monica Cisneros introducing herself as the Senior Product Marketing Manager for Windows, joined by Scott Hanselman (00:00:01).

### [LIVE145] Coding and Personal Agents with Ollama
*Speakers:* Michael Chiang, John Maeda, Parth Sareen  
[Session page](https://build.microsoft.com/en-US/sessions/LIVE145) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/f6e2dbf7-2eac-48a8-ac0f-9c687945de59) · [Video](https://medius.microsoft.com/Embed/video-nc/f6e2dbf7-2eac-48a8-ac0f-9c687945de59)

- The team previews an upcoming breakout session showcasing live demos and more agentic task examples 00:10:00–00:10:12.

### [LIVE151] Extend GitHub Copilot with the Copilot SDK
*Speakers:* Burke Holland, Patrick Nikoletich  
[Session page](https://build.microsoft.com/en-US/sessions/LIVE151) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/175f1178-984b-4d72-b15b-108d8d67dec2) · [Video](https://medius.microsoft.com/Embed/video-nc/175f1178-984b-4d72-b15b-108d8d67dec2)

- Patrick notes the SDK’s general availability (GA) status, announced just the day before, marking a major milestone for developers across Microsoft and its subsidiaries like LinkedIn, Xbox, and GitHub.
- New SDK features like remote access, ephemeral cloud sandboxes, and local sandbox environments are now available for preview, offering developers flexibility to prototype without heavy setup 00:12:01–00:12:19.
- Patrick invites attendees to his upcoming session from 4:00–5:00 PM in Breakout 1 for a deeper technical dive into the Copilot SDK’s future and cross-Microsoft integration 00:15:08–00:15:25.

### [LIVE156] Designing VS Code’s UX for the Agentic Era
*Speakers:* Burke Holland, Joanna Oikawa  
[Session page](https://build.microsoft.com/en-US/sessions/LIVE156) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/705403fe-f8ee-43bd-a13d-b49502401ad9) · [Video](https://medius.microsoft.com/Embed/video-nc/705403fe-f8ee-43bd-a13d-b49502401ad9)

- The conversation at 00:02:45 reveals that these decisions are informed by user research and telemetry, focusing on how developers engage with sessions and projects.
- She stresses the importance of validation—testing whether quick fixes and new features actually serve their purpose rather than just adding noise.

### [LIVE168] Claude Is in Copilot. Here's What That Actually Means
*Speakers:* Burke Holland, Tyler Leonhardt  
[Session page](https://build.microsoft.com/en-US/sessions/LIVE168) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/13f19aee-b872-4a65-8156-2ae9842c4178) · [Video](https://medius.microsoft.com/Embed/video-nc/13f19aee-b872-4a65-8156-2ae9842c4178)

- The conversation quickly pivots toward the main topic — exploring new features in VS Code that incorporate Claude agents, signaling a shift from the more familiar Copilot focus at 00:00:30.
- Conversation on Real-World Use and Demonstration Setup: Adding personality to the discussion, Tyler reveals he organizes local improv events and demonstrates using Copilot and Claude together to generate a website for an event called "Compliment Fest" (00:03:39).

### [ODSP906] Apply orchestration patterns for production AI agents
*Speakers:* Cliff Simpkins  
[Session page](https://build.microsoft.com/en-US/sessions/ODSP906) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/716ac10b-3253-4e07-af14-68866af36f67) · [Video](https://medius.microsoft.com/Embed/video-nc/716ac10b-3253-4e07-af14-68866af36f67)

- Exploring Maestro Flow and Enterprise Process Modeling: Beginning at 00:08:12, Vikram Kakumani and Milo Shields introduce Maestro Flow—the new visual canvas for developers.

### [ODSP923] Create enterprise apps with AI and MCP
*Speakers:* Jason Beres  
[Session page](https://build.microsoft.com/en-US/sessions/ODSP923) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/ca45af6a-86b5-4082-921a-c2c8f5fe346e) · [Video](https://medius.microsoft.com/Embed/video-nc/ca45af6a-86b5-4082-921a-c2c8f5fe346e)

- Introduction and Overview: The presenter, Jason Beres, begins by introducing the topic of creating enterprise applications leveraging AI and low-code capabilities (00:00:01–00:00:11).
- He also announces the launch of a new WinUI component suite introduced at Build 2026 (00:01:55–00:02:03), highlighting support for MAUI as part of their cross-platform approach.
- Exploration of Products and App Builder Overview: Jason shows how visitors can learn more about Infragistics products such as UI components, Reveal for embedded analytics, and Slingshot for AI-native work management from the company website (00:02:34–00:02:52).

### [ODSP929] Build modern .NET apps with Uno Platform, AI, and visual tools
*Speakers:* Sam Basu  
[Session page](https://build.microsoft.com/en-US/sessions/ODSP929) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/007f6aac-9c60-4853-b8e9-b4bfba63ec1d) · [Video](https://medius.microsoft.com/Embed/video-nc/007f6aac-9c60-4853-b8e9-b4bfba63ec1d)

- In closing, Sam invites attendees to meet the Uno Platform team at Microsoft Build, attend their theater sessions in collaboration with Kahua, and explore upcoming announcements (00:18:26).

---

## Agents

_Agent platforms and patterns — Agent 365, Autopilot, Scout, Claw + Agent Harness, OpenClaw, MCP, Toolbox, ACS, ASSERT_

### [BRK201] Multi-agent patterns in VS Code you won't learn from docs
*Speakers:* Pierce Boggan, Kent C. Dodds, Burke Holland, Julia Kasper, Harald Kirschner, Chris Reddington  
[Session page](https://build.microsoft.com/en-US/sessions/BRK201) · [Video](https://medius.microsoft.com/Embed/video-nc/c3a80714-e18b-4cd1-b75c-92204129a14d)

- Contestants and Tools Overview: The competition’s participants are introduced along with the tools they will use 00:03:52.
- The closing remarks emphasize the difficulty of live coding, appreciation for the participants, and encourage attendees to join upcoming Copilot and multi-agent sessions, thanking everyone for attending 00:46:13.

### [BRK202] Azure DevOps meets GitHub, the path to AI powered SDLC
*Speakers:* Dave Burnison, Dan Hellem, Lan Kaim  
[Session page](https://build.microsoft.com/en-US/sessions/BRK202) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/ce405956-4847-4b45-a5e6-e2fa334f2cfe) · [Video](https://medius.microsoft.com/Embed/video-nc/ce405956-4847-4b45-a5e6-e2fa334f2cfe)

- Dan then unveils Copilot Auto Fix for GitHub Advanced Security 00:36:00–00:37:40, which allows dynamic background pipeline processing to automatically generate secure code updates and pull requests using CodeQL scans.

### [BRK207] GitHub Copilot in Visual Studio: Agents That Debug, Profile, and Test
*Speakers:* Nik Karpinsky, Mads Kristensen, Anisha Pindoria  
[Session page](https://build.microsoft.com/en-US/sessions/BRK207) · [Video](https://medius.microsoft.com/Embed/video-nc/45d559ef-d829-4eda-a101-b034bea5bcb3)

- Upcoming Features and Roadmap: In the later part of the talk (00:33:00–00:41:00), Matt outlines several upcoming Visual Studio and Copilot capabilities.
- They close with encouragement to try the upcoming Insider builds of Visual Studio 2026, highlighting the broad innovation pipeline extending through the summer and inviting developers to test new features first-hand.

### [BRK225] Data, apps, and agents: the future of app dev with Rayfin
*Speakers:* Sachin Patney, Ben Zulauf  
[Session page](https://build.microsoft.com/en-US/sessions/BRK225) · [Video](https://medius.microsoft.com/Embed/video-nc/c1caffa3-94c6-4ba4-92e3-1aef6b91878d)

- Introducing Raefen – The AI Coding Backend: Addressing these gaps, Ben introduces Raefen as a backend framework for the AI coding era 00:02:34.
- Partnerships, Future Roadmap, and Conclusion: To make Raefen accessible beyond traditional IDE users, Microsoft announced a partnership with Replit, represented by Carl, who demonstrates how non-technical users can build analytic dashboards directly within Replit using Raefen and Fabric integration 00:26:01.
- Ben returns to conclude by outlining Raefen’s roadmap—upcoming features include function support, RBAC, enhanced connectors, and integration with OneLake 00:28:32.

### [BRK228] Modern resiliency from build to recovery through Agentic AI
*Speakers:* Rochak Mittal, Adity Agarwal, Shobhit Garg  
[Session page](https://build.microsoft.com/en-US/sessions/BRK228) · [Video](https://medius.microsoft.com/Embed/video-nc/35984817-c07b-4b72-a5f0-2f8a6803325d)

- Introduction and Core Principles: The session begins with Abhimanyu, joined by Aditi and Shobhit, introducing the theme of resiliency and new agent capabilities designed to help users identify and mitigate gaps in their systems (00:00:05).
- Unified Resiliency Management and Public Preview Announcements: The speakers highlight the evolution from Azure Business Continuity Center to a unified “Azure Resiliency” platform announced at Ignite (00:05:11).
- They introduce the concept of service groups, which shift planning from individual resources to entire applications, reflecting a business-centric resilience model.
- New additions include the Resiliency Manager public preview—providing zonal resiliency management, automated goal assignments, continuous health checks, and simulated resiliency drills powered by Chaos Studio (00:07:00), allowing developers to test and improve their failover readiness through real-world failure simulations.
- A subsequent section reveals AI-powered prioritization in Azure Advisor, where recommendations are ranked based on factors such as blast radius, deadlines, and cost (00:33:23).
- Staying Resilient and Final Announcements: The closing section emphasizes the importance of continuous validation through simulated fault conditions.
- At Build, Microsoft announces the public preview of Azure Chaos Studio Workspaces launching June 11 (00:44:00), a new application-centric environment for resilience testing.

### [DEM301] Rethinking CI: Actions, AI Agents, and the End of Commit-Fail-Commit
*Speakers:* Salil Subbakrishna, Denizhan Yigitbas  
[Session page](https://build.microsoft.com/en-US/sessions/DEM301) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/079bf23f-302e-4b23-bc15-add6bb85deee) · [Video](https://medius.microsoft.com/Embed/video-nc/079bf23f-302e-4b23-bc15-add6bb85deee)

- Introducing the Actions Debugger: After showing how agentic workflows handle automated analysis, Salil transitions to the upcoming Actions Debugger, designed for deeper human-in-the-loop investigation when workflows behave unpredictably 00:10:49.
- Roadmap, Availability, and Closing Remarks: The presentation wraps up with announcements on release timelines 00:20:40.
- Agentic workflows will enter public preview the following week, supported by documentation and quick-start examples for issue management, documentation automation, and multi-repository orchestration.

### [DEM351] AI Skills Navigator: Accelerate tech skills with personalized learning
*Speakers:* Shreenidhi Bindinganavile Ramanuja, Matt Erni  
[Session page](https://build.microsoft.com/en-US/sessions/DEM351) · [Video](https://medius.microsoft.com/Embed/video-nc/9dbfe949-af78-47ce-b6ed-97552be1217b)

- They encourage viewers to register, personalize their profiles, and join the upcoming “Skills Fest” event taking place June 8–12 as a next step in advancing their AI learning journey (00:22:21).

### [DEMSP382] Build AI Apps with Oracle AI Database@Azure, MCP, and GitHub Copilot
*Speakers:* Rajya Laxmi Yellajosyula, Partha Srinivasan  
[Session page](https://build.microsoft.com/en-US/sessions/DEMSP382) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/c0c8d8d2-d75e-491a-857e-be570cdbd42f) · [Video](https://medius.microsoft.com/Embed/video-nc/c0c8d8d2-d75e-491a-857e-be570cdbd42f)

- Oracle Database on Azure is introduced as a native service available through the Azure Marketplace, enabling seamless integration in development environments 00:01:16–01:01:24.

### [LIVE149] Day 1 Recap: What You Missed (or Watched Twice)
*Speakers:* Pierce Boggan, Burke Holland  
[Session page](https://build.microsoft.com/en-US/sessions/LIVE149) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/4b5c196a-6068-418a-81e9-a122f5107c15) · [Video](https://medius.microsoft.com/Embed/video-nc/4b5c196a-6068-418a-81e9-a122f5107c15)

- Announcements and Community Engagement: Following introductions, Burke outlines several announcements and event highlights for attendees 00:00:43–00:00:52.
- Pierce amusingly reveals he will be “locked in” for a live coding session later, continuing the playful banter.
- Sessions and Fun Events: Burke then promotes upcoming sessions including the “VS Code team’s AI adoption story” led by Pierce and Josh 00:01:47–00:02:01.

### [LIVE154] Your Browser Lives in VS Code Now
*Speakers:* Justin Chen, Burke Holland  
[Session page](https://build.microsoft.com/en-US/sessions/LIVE154) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/cc424a49-15c3-479e-99d9-830cac9021ca) · [Video](https://medius.microsoft.com/Embed/video-nc/cc424a49-15c3-479e-99d9-830cac9021ca)

- He introduces Justin from the Visual Studio Code (VS Code) team, setting the stage for a discussion focused on new features developed for the popular editor.

### [LIVE169] The New Agents Window in VS Code
*Speakers:* Burke Holland, Harald Kirschner  
[Session page](https://build.microsoft.com/en-US/sessions/LIVE169) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/39e7b927-a96f-4e0c-bc26-8d9fb757cd58) · [Video](https://medius.microsoft.com/Embed/video-nc/39e7b927-a96f-4e0c-bc26-8d9fb757cd58)

- Introducing the Agent Window Concept: The talk transitions at 00:01:02 to focus on the new "agent window," previously called the "agent sessions window." Harold describes how it evolved to streamline work with multiple coding agents and projects.
- He shares his setup using VS Code customization hooks to trigger spoken summaries through local speech models when a task completes—his computer announces completion details aloud 00:06:33.
- Cost Optimization and Model Routing: Near the session’s close at 00:07:31, Harold introduces cost and performance improvements tied to new model usage in VS Code’s AI features.

### [LIVESP128] From local AI PCs to Azure: The future of open-source AI development
*Speakers:* Adrian Macias  
[Session page](https://build.microsoft.com/en-US/sessions/LIVESP128) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/4f44c7a4-7e1a-4fc3-b614-690604749d97) · [Video](https://medius.microsoft.com/Embed/video-nc/4f44c7a4-7e1a-4fc3-b614-690604749d97)

- Creativity, Announcements, and Conclusion: Adrian reflects on how these technological changes unleash creativity in developers, stating that innovation is directly linked to iteration speed 00:10:20.

### [OD801] Modernize intelligent apps and agents with .NET that scale as you grow
*Speakers:* Gaurav Seth, Andrew Westgarth  
[Session page](https://build.microsoft.com/en-US/sessions/OD801) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/d14b3177-b1c2-481c-9094-4fe12dc84b75) · [Video](https://medius.microsoft.com/Embed/video-nc/d14b3177-b1c2-481c-9094-4fe12dc84b75)

- The agenda covers app modernization challenges, the previously launched Managed Instance on Azure App Service from Ignite (00:00:58), the newly introduced Built-In MCP at Build (00:01:18), the GitHub Copilot modernization tooling, and a live demonstration by Gaurav followed by closing resources and insights on cloud transformation.
- Introducing Built-In MCP and Agentic Patterns: The session reveals a major new capability—Built-In MCP—unveiled at Build (00:13:03).

### [OD806] .NET 11 in depth: Runtime, libraries, and SDK for the AI era
*Speakers:* —  
[Session page](https://build.microsoft.com/en-US/sessions/OD806) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/06f91e84-cd18-4043-b4b6-c4ac9b0d2b0e) · [Video](https://medius.microsoft.com/Embed/video-nc/06f91e84-cd18-4043-b4b6-c4ac9b0d2b0e)

- The team also unveils `.NET Up`, a native AOT acquisition tool that simplifies SDK version management across platforms without administrative permissions.
- The talk closes with Rich and Chet emphasizing how developers can experiment with these preview features now, provide GitHub feedback, and help optimize .NET 11 for its upcoming general release.

### [ODSP911] Build AI-first business apps that turn dashboards into actions
*Speakers:* Paul Usher  
[Session page](https://build.microsoft.com/en-US/sessions/ODSP911) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/8041cdaf-f3df-44ea-aa33-0dd7e1dd2745) · [Video](https://medius.microsoft.com/Embed/video-nc/8041cdaf-f3df-44ea-aa33-0dd7e1dd2745)

- Within Visual Studio, Paul reveals how this functionality is enabled via “AddBlazorReportingAIIntegration” calls in Program.cs.

### [ODSP918] Build persistent and scalable AI agent memory with TiDB
*Speakers:* Ravish Patel  
[Session page](https://build.microsoft.com/en-US/sessions/ODSP918) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/2ba4cfc6-63e4-4c2c-bedc-0884e1141a16) · [Video](https://medius.microsoft.com/Embed/video-nc/2ba4cfc6-63e4-4c2c-bedc-0884e1141a16)

- Introduction and Problem Context: The video begins with Ravish Patel introducing himself as a solutions engineer at PingCAP working on TiDB (00:00:03).

### [ODSP937] Build realtime multimodal agents with LiveKit and Azure
*Speakers:* Jesse Hall  
[Session page](https://build.microsoft.com/en-US/sessions/ODSP937) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/08898b31-c2d7-4d94-84c5-14f9e0e70cef) · [Video](https://medius.microsoft.com/Embed/video-nc/08898b31-c2d7-4d94-84c5-14f9e0e70cef)

- The session’s focus is announced — exploring LiveKit, the cascaded pipeline, and how Azure integrates with LiveKit 00:00:27–00:00:37.

---

## Windows

_Windows for developers and agents — WSL Containers, Surface RTX Spark, Copilot+ PCs, on-device AI, Windows ML_

### [BRK261] Build and ship faster with a developer-optimized experience on Windows
*Speakers:* Kayla Cinnamon, Craig Loewen, Clint Rutkas  
[Session page](https://build.microsoft.com/en-US/sessions/BRK261) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/9574001f-c87e-401e-9e24-87990c6318f9) · [Video](https://medius.microsoft.com/Embed/video-nc/9574001f-c87e-401e-9e24-87990c6318f9)

- She highlights upcoming desktop features, such as movable taskbars, integrated into the Windows Insider program, and an upgraded Run dialog that now uses PowerToys Command Palette architecture.
- He also reveals “Coreutils for Windows” 00:08:23, which brings over 160 common Linux command-line tools (e.g., grep, tail, env) natively to Windows.
- Integration of Containers APIs and Partner Collaborations: In the later portion (00:32:31), Craig revisits WSL containers to introduce the WSL Containers API and its integration into Windows apps.

### [DEM311] Scale cloud-native workloads with Azure Linux
*Speakers:* Poorvi Narang, Jim Perrin  
[Session page](https://build.microsoft.com/en-US/sessions/DEM311) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/1b886f16-d29b-4873-a32c-b8002baa7b46) · [Video](https://medius.microsoft.com/Embed/video-nc/1b886f16-d29b-4873-a32c-b8002baa7b46)

- Azure Container Linux 3.0 is now generally available, with version 4.0 entering preview alignment.
- The presenters summarize product availability: Azure Linux 4.0 in public preview, with Azure Container Linux officially GA.

### [DEM334] Build agents where work happens: chats, channels, and meetings in Microsoft Teams
*Speakers:* Lily Du, Umang Sehgal  
[Session page](https://build.microsoft.com/en-US/sessions/DEM334) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/b230adf8-4c48-4bb1-9114-6c6bfd355318) · [Video](https://medius.microsoft.com/Embed/video-nc/b230adf8-4c48-4bb1-9114-6c6bfd355318)

- Lily announces several enhancements under "manners," such as emoji reactions, quoted replies, and threaded replies (00:08:26–00:09:41).

### [LIVE115] Scott and Mark learn to Vibe Check with Swyx
*Speakers:* swyx (Shawn Wang), Scott Hanselman  
[Session page](https://build.microsoft.com/en-US/sessions/LIVE115) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/e52b8eb8-f1d1-4659-9e59-f1754039b9a1) · [Video](https://medius.microsoft.com/Embed/video-nc/e52b8eb8-f1d1-4659-9e59-f1754039b9a1)

- Introduction and Context: At the start of the video 00:00:00–00:00:06, Scott and Mark introduce a segment of "Scott and Mark Learn to Vibe" taking place live at Microsoft Build.
- He describes the app as something he’s slightly nervous to reveal since it’s under development but actively being used by his team.

---

## Developer Tools

_GitHub + VS Code + GitHub Copilot — CLI, Copilot app, Auto Fix, Azure DevOps integration, agentic SDLC_

### [BRK204] What we learned shipping VS Code weekly (without breaking everything)
*Speakers:* Pierce Boggan, Josh Spicer, Anna Soracco  
[Session page](https://build.microsoft.com/en-US/sessions/BRK204) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/8e6c2160-2e93-40ac-8b17-a731909983b0) · [Video](https://medius.microsoft.com/Embed/video-nc/8e6c2160-2e93-40ac-8b17-a731909983b0)

- Rather than announcing a new product, the goal is to share how the team’s engineering systems and processes evolved to handle AI-driven development.

### [DEM305] GitHub Copilot Anywhere: From Remote Control CLIs to Cloud Sandboxes
*Speakers:* Ellie Bennett, Denizhan Yigitbas  
[Session page](https://build.microsoft.com/en-US/sessions/DEM305) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/c8128017-96b9-476c-9004-8ba91e2ef3cd) · [Video](https://medius.microsoft.com/Embed/video-nc/c8128017-96b9-476c-9004-8ba91e2ef3cd)

- He unveils "Cloud Sandbox" for Copilot, now in public preview (00:10:22–00:10:45).
- Chronicle Feature and Conclusion: Ellie closes the session by introducing "Chronicle," a meta-feature that logs and indexes all user Copilot sessions for insights, tips, and enhancements across platforms like CLI, VS Code, JetBrains, and github.com (00:19:57–00:21:09).

### [DEM332] From zero to teammate in 25 minutes: Build a Teams agent live
*Speakers:* Aamir Jawaid, Umang Sehgal  
[Session page](https://build.microsoft.com/en-US/sessions/DEM332) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/901bde6f-0064-4018-891f-4b8fbaba8d71) · [Video](https://medius.microsoft.com/Embed/video-nc/901bde6f-0064-4018-891f-4b8fbaba8d71)

- SDK Evolution and Simplification Goals: Umang explains that last year’s Build introduced the Teams AI library in TypeScript and C#, while this year’s focus is on the new integrated Teams SDK (00:01:15).
- He previews upcoming group UX features such as emoji reactions, targeted messages, slash commands, quoted replies, and markdown support, enhancing collaborative experiences with intelligent agents inside Teams (00:14:10).

### [LIVE152] What's new in GitHub Copilot CLI?
*Speakers:* Evan Boyle, Burke Holland  
[Session page](https://build.microsoft.com/en-US/sessions/LIVE152) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/609cb95c-6575-4206-9586-c26853e87efd) · [Video](https://medius.microsoft.com/Embed/video-nc/609cb95c-6575-4206-9586-c26853e87efd)

- Evan Boyle from the GitHub Copilot CLI team is introduced as a guest and described as both an engineering manager and hands-on developer passionate about developer tools (00:00:34).
- Closing and Next Steps: As the session concludes, Evan announces upcoming talks, including one later that day on the GitHub app with Mario and another recorded deep dive with Cassidy on Copilot CLI (00:16:25).

### [LIVE162] From issue to merge in one loop: the GitHub Copilot app
*Speakers:* Burke Holland, Seth Juarez  
[Session page](https://build.microsoft.com/en-US/sessions/LIVE162) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/4ab34223-dd67-4829-846d-ca53fe37892b) · [Video](https://medius.microsoft.com/Embed/video-nc/4ab34223-dd67-4829-846d-ca53fe37892b)

- Introducing GitHub Copilot and Workflow Contexts: The hosts shift to explaining how GitHub Copilot fits into different developer workflows.
- They celebrate simplicity and accessibility, joking that everything now moves “so slowly and it’s so easy to understand all the new features” (00:14:01).

### [LIVE199] Imagine Cup World Championship
*Speakers:* Patrick Brown, Rohan Ganesh, Surya Kukkapalli, Troy McBride, Vivaan Sawant, Advika Vuppala, Hans Yang  
[Session page](https://build.microsoft.com/en-US/sessions/LIVE199) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/e4271f82-0b86-40ab-a575-c7596029ed2e) · [Video](https://medius.microsoft.com/Embed/video-nc/e4271f82-0b86-40ab-a575-c7596029ed2e)

- Donna introduces the prestigious judging panel and announces that the winning team will receive $100,000 and a mentorship session with Satya Nadella (00:03:01).
- Finalist Introductions and Projects Overview: The video transitions to short documentary-style vignettes introducing each finalist and their projects.
- Announcement and Conclusion: As the excitement peaks, Donna and Hans congratulate the teams and acknowledge their mentors for helping shape their journeys (00:15:03).
- Hans reveals a surprise announcement: Microsoft has increased the grand prize from $100,000 to $150,000 (00:16:07).

### [OD804] Simplifying .NET Installs with dotnetup
*Speakers:* —  
[Session page](https://build.microsoft.com/en-US/sessions/OD804) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/bb273074-b360-4724-bb2f-31167ffe2b19) · [Video](https://medius.microsoft.com/Embed/video-nc/bb273074-b360-4724-bb2f-31167ffe2b19)

- The roadmap includes internal preview, public preview, and GA milestones 00:38:06–00:41:02.
- Public preview will add self-updating behavior, signed validation, and integration with agent skill repositories for automation 00:41:19–00:43:07.

### [OD810] Build fast, not fragile with Rayfin and Microsoft Fabric
*Speakers:* Yohan Lasorsa  
[Session page](https://build.microsoft.com/en-US/sessions/OD810) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/8d61253f-f0fa-49ee-9f91-10e852b48f42) · [Video](https://medius.microsoft.com/Embed/video-nc/8d61253f-f0fa-49ee-9f91-10e852b48f42)

- Introducing Rayfin and Session Roadmap: The talk transitions to the introduction of Rayfin — a managed backend-as-a-service built on Microsoft Fabric, designed to bridge the gap between prototype and production 00:02:48–00:03:03.
- From Prototype to Production: After showing the MVP working locally, Lasorsa reveals that production deployment has been silently achieved through the same “Rayfin app” command 00:28:01–00:28:36.

---

## Security + Governance

_Agent governance and security — Agent 365, Purview, Defender, Entra, ASSERT, ACS, evaluation frameworks_

### [LIVE141] Programming robots
*Speakers:* Chip Huyen, John Maeda  
[Session page](https://build.microsoft.com/en-US/sessions/LIVE141) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/0a938684-4ae8-403c-9495-2138587205d5) · [Video](https://medius.microsoft.com/Embed/video-nc/0a938684-4ae8-403c-9495-2138587205d5)

- Guidance for Developers and Industry Safety Lessons: Moving from research to application, Chip advises developers to stay focused instead of chasing every AI advance or funding announcement 00:09:27–00:10:37.

### [ODSP926] Build collaborative agents into apps with APIs
*Speakers:* Ziv Navoth, Edo Segal, Gillian Sheldon  
[Session page](https://build.microsoft.com/en-US/sessions/ODSP926) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/fea669e6-5140-4ea8-b097-a765d61311ee) · [Video](https://medius.microsoft.com/Embed/video-nc/fea669e6-5140-4ea8-b097-a765d61311ee)

- He reveals that the Omniagent API runs at merely one cent per render minute when developers use their own large language models — about twenty times cheaper than competing solutions.
- Knowledge bases containing manuals and diagnostic data are attached, FAQs for safety and service routines are extended, and new tools like customer lookup are added.

---

## Other / Cross-cutting

### [DEM376] The story of the Global AI Community that spans every continent
*Speakers:* Roelant Dieben, Stephen Simon  
[Session page](https://build.microsoft.com/en-US/sessions/DEM376) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/9b441553-0170-41c9-9cc5-34040734f410) · [Video](https://medius.microsoft.com/Embed/video-nc/9b441553-0170-41c9-9cc5-34040734f410)

- The presenters proudly announce milestones: over 200,000 registered members, 200 global chapters, and more than 4,600 events conducted to date 00:02:36–00:02:56.

### [LIVE116] Scott and Mark learn to Vibe Check with Steve Sanderson
*Speakers:* Scott Hanselman, Steve Sanderson  
[Session page](https://build.microsoft.com/en-US/sessions/LIVE116) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/412eb4f9-6245-4b44-9497-dd6019195fe5) · [Video](https://medius.microsoft.com/Embed/video-nc/412eb4f9-6245-4b44-9497-dd6019195fe5)

- The hosts build suspense by suggesting Steve will unveil something entirely new—perhaps created in a playful, AI-driven coding spree.
- He launches standard applications—Notepad, Calculator, and Internet Explorer—but reveals a key twist: none of these apps contain any code.

### [ODSP902] Build AI‑driven UIs in .NET MAUI with design systems
*Speakers:* Shriram Sankaran, Vishnu Menon  
[Session page](https://build.microsoft.com/en-US/sessions/ODSP902) · [Transcript](https://medius.microsoft.com/video/asset/Transcript/d2ae05f2-1269-4f1c-aaa0-888f9b8d4e7a) · [Video](https://medius.microsoft.com/Embed/video-nc/d2ae05f2-1269-4f1c-aaa0-888f9b8d4e7a)

- The difference between outputs “with skills” and “without skills,” highlighted at 00:06:23–00:06:48, reveals that an AI guided by skills creates more consistent, design-aware interfaces.

---

## Public Microsoft Build 2026 News (mirror)

_The following is mirrored verbatim from the public [`microsoft/Build26-news`](https://github.com/microsoft/Build26-news/blob/main/news.md) repository, Microsoft's canonical announcement index._

# Microsoft Build 2026 — What's New

Structured index of announcements from Microsoft Build 2026 (June 2, 2026). Each statement uses exact wording from the source blog.

---


---

# Microsoft Build 2026 — Batch 1: OMB + HERO Blogs (Tier 1+2 Full Extraction)

---

## Blog 1: OMB Developer Blog

### 1. Microsoft IQ — Context Layer
**Products**: Microsoft IQ, Work IQ, Fabric IQ, Foundry IQ, Web IQ
**Blog**: https://aka.ms/AA10pe80

1. **Microsoft IQ**: "generally available this month across GitHub Copilot, Microsoft Foundry and Copilot Studio, is a new context layer that grounds agents in both world knowledge and enterprise knowledge"
2. **Work IQ**: "the workplace intelligence layer for agents, capturing how work actually happens across Microsoft 365, organizational systems and external sources: people, emails, documents, meetings and how they connect"
3. **Work IQ APIs**: "generally available on June 16, provide programmatic access to this intelligence layer and give agents the context they need to work effectively in your organization"
4. **Fabric IQ**: "provides a shared semantic foundation over structured business data"
5. **Foundry IQ**: "ties it together and enables retrieval planning across both enterprise knowledge and the live web"
6. **Web IQ**: "the fastest real-world grounding you can give your agents. An AI-first web search stack that's model-agnostic and MCP-native, returning relevant passages at nearly 2.5x the speed of the next best alternative"

### 2. Microsoft Scout
**Products**: Microsoft Scout, OpenClaw, WorkIQ
**Blog**: https://aka.ms/AA10pe80

1. **Microsoft Scout**: "a new personal agent for work that we are bringing to Frontier customers today"
2. **Microsoft Scout**: "Built on OpenClaw and WorkIQ, Microsoft Scout understands how you work, uses the tools you already live in, like Teams and Outlook, and proactively handles things like meeting prep, scheduling conflicts and routine tasks without asking"

### 3. MAI Model Family
**Products**: MAI-Thinking-1, MAI-Image-2.5, MAI-Voice-2, MAI-Transcribe 1.5, MAI-Code-1
**Blog**: https://aka.ms/AA10pe80

1. **MAI-Thinking-1**: "Microsoft AI's first reasoning model. Trained from scratch with zero distillation on enterprise grade, clean and commercially licensed data you can build on with confidence"
2. **MAI-Thinking-1**: "a mid-sized, 35 billion active parameter model with a 256K context window built for high efficiency and performance, but importantly, at a low-token cost"
3. **MAI-Thinking-1**: "On a blind test, independent raters prefer it to Sonnet 4.6, and it matches Opus 4.6 on coding abilities on SWE Bench Pro"
4. **MAI-Thinking-1**: "designed to be good at complex multi-step instructions, long-context reasoning and code generation, and it's open now on Foundry in private preview"
5. **MAI-Image-2.5**: "Microsoft's first models to serve both text-to-image (#3 on the Arena AI leaderboard) and enabling image-to-image workloads (#2 on the Arena AI leaderboard, surpassing Nano Banana 2)"
6. **MAI-Image-2.5**: "These models are live in PowerPoint, rolling out on OneDrive, and today, they're landing on Foundry with market-leading quality per dollar"
7. **MAI Transcribe 1.5**: "combines state-of-the-art accuracy across 43 languages, with streaming coming soon"
8. **MAI-Voice-2**: "now available in more than 15 additional languages with new voice options"
9. **MAI-Code-1**: "our inference efficient coding model tuned for GitHub, is now available in Copilot and VS Code"
10. **MAI models on third-party platforms**: "MAI models will also be available on Fireworks AI, Baseten and Open Router"

### 4. Fireworks AI on Foundry
**Products**: Fireworks AI, Microsoft Foundry
**Blog**: https://aka.ms/AA10pe80

1. **Fireworks AI on Foundry**: "now generally available on Foundry, giving developers a single platform experience with enterprise governance and Azure data residency, regardless of the model they choose"

### 5. Frontier Tuning
**Products**: Frontier Tuning
**Blog**: https://aka.ms/AA10pe80

1. **Frontier Tuning**: "applies reinforcement learning within your compliance boundary so agents can learn how the business actually works"
2. **Frontier Tuning**: "Using your own data, domain knowledge and workflows, the result is a loop that sharpens as agents work. Available in private preview today"

### 6. Agent Security and Governance
**Products**: Agent 365, Entra, Defender, Purview, ASSERT, Agent Control Specification, Codename MDASH
**Blog**: https://aka.ms/AA10pe80

1. **Agent 365 for local agents**: "extends capabilities to observe, govern and secure local agents across your estate, including more than 20 types of local agents."
2. **ASSERT**: "an open-source project for policy-driven safety evaluation"
3. **Agent Control Specification**: "to standardize where and how to apply controls in the agent loop"
4. **Codename MDASH**: "Our new multi-model agentic security system deploys 100+ agents to find exploitable bugs by reasoning about data flow, business logic and exploit chains with context-aware fixes delivered directly in the Defender Portal"

### 7. Surface RTX Spark Dev Box
**Products**: Surface RTX Spark Dev Box, NVIDIA RTX Spark
**Blog**: https://aka.ms/AA10pe80

1. **Surface RTX Spark Dev Box**: "designed for sustained workloads: long-running training jobs, agentic AI pipelines and local model fine-tuning"
2. **Surface RTX Spark Dev Box**: "delivers up to one petaflop of AI compute and 128 GB of unified memory, capable of running up to 120B parameter LLMs with up to 1 million tokens context using agents locally without cloud GPU instances"
3. **Surface RTX Spark Dev Box**: "WSL 2 with GPU passthrough and full CUDA support comes pre-configured for developers, with Visual Studio Code, GitHub Copilot and many more of your favorite tools installed"
4. **Surface RTX Spark Dev Box**: "will be available later this year in the US via Microsoft.com"

### 8. Microsoft Execution Containers (MXC)
**Products**: Microsoft Execution Containers (MXC), OpenClaw on Windows, NVIDIA OpenShell
**Blog**: https://aka.ms/AA10pe80

1. **Microsoft Execution Containers (MXC)**: "now in preview, gives developers and IT administrators a simpler way to create enterprise-grade sandboxed environments for agents, with containment enforced by the operating system itself"
2. **OpenClaw on Windows**: "enabling execution of multi-step workflows inside these OS-enforced boundaries"
3. **NVIDIA OpenShell**: "secure runtime for autonomous agents uses MXC and adds policy management, inference routing and PII obfuscation"

### 9. Hosted Agents in Foundry Agent Service
**Products**: Foundry Agent Service
**Blog**: https://aka.ms/AA10pe80

1. **Hosted agents in Foundry Agent Service**: "in preview, provide the same model at scale: instant-on sandboxes per session, isolated execution, persistent memory and elastic scale"
2. **Hosted agents in Foundry Agent Service**: "Think of it as the primitive for agents the way containers were for cloud-native apps"

### 10. GitHub Copilot App
**Products**: GitHub Copilot app
**Blog**: https://aka.ms/AA10pe80

1. **GitHub Copilot app**: "now in preview, brings agentic development to a native desktop experience – and a much wider audience"
2. **GitHub Copilot app**: "Start from an idea, an existing issue or PR, orchestrate multiple agent sessions in parallel, and keep changes moving through review, CI and merge. Each session uses git worktrees, so work stays separated"

### 11. Project Rayfin
**Products**: Project Rayfin, Replit, Azure HorizonDB
**Blog**: https://aka.ms/AA10pe80

1. **Project Rayfin**: "now in preview, solves that. It brings a managed, backend-as-a-service to Microsoft Fabric, defined through GitHub-based workflows, so developers can move from prototype to production without managing infrastructure"
2. **Replit integration**: "creates a fast path from prototype to enterprise-grade deployment with governance from day one"
3. **Azure HorizonDB**: "a fully managed PostgreSQL service on Azure that delivers more than 3x the throughput of comparable self-managed setups in internal testing"

### 12. Microsoft Discovery
**Products**: Microsoft Discovery
**Blog**: https://aka.ms/AA10pe80

1. **Microsoft Discovery**: "generally available today. Built on Azure, it gives researchers an enterprise-grade agentic AI platform for the full science workflow"
2. **Microsoft Discovery**: "BHP is using it to find copper-leaching solutions in months instead of years. Syensqo is accelerating semiconductor R&D. GSK is iterating on drug discovery"
3. **Discovery local app**: "a free Discovery local app was announced for the broader scientific community. It is available in preview and only requires a GitHub Copilot account"

### 13. Majorana 2
**Products**: Majorana 2
**Blog**: https://aka.ms/AA10pe80

1. **Majorana 2**: "an average qubit lifetime of 20 seconds with instances up to a minute, 1,000x higher reliability than our previous generation, and a path to one million qubits on a chip that fits in the palm of your hand"
2. **Majorana 2**: "With the help of agentic AI, we will achieve a scalable quantum machine by 2029"

### 14. Microsoft Agent Platform — Themes
**Products**: Microsoft Agent Platform, Microsoft Foundry, GitHub, Microsoft Teams, M365
**Blog**: https://aka.ms/AA10pe80

1. **Microsoft Agent Platform**: "you can build your agent in GitHub, deploy it to Microsoft Foundry and optimize it automatically with models best suited for the job"
2. **Windows for developers**: "a new developer configuration that gives you more flexibility, a frictionless intelligent shell and terminal experience, local sandboxing for agents, new Windows Subsystem for Linux capabilities and powerful options to do it on your local machine"

---

## Blog 2: HERO — Quantum + Discovery

### 15. Majorana 2 — Quantum Computing
**Products**: Majorana 2
**Blog**: https://aka.ms/AA10vjcq

1. **Majorana 2**: "its next-generation topological quantum chip developed with the help of Microsoft Discovery's agentic AI"
2. **Majorana 2 materials stack**: "a new materials stack enabling a 1,000-fold improvement in reliability over the prior generation of qubits, with a mean qubit lifetime of 20 seconds and instances lasting as long as one minute"
3. **Majorana 2 timeline**: "Microsoft now expects to achieve a scalable quantum computer by 2029, cutting its original timeline in half"
4. **Majorana 2 qubit operations**: "fast speed (one microsecond operations) and small qubit size (1/100th of a millimeter)"
5. **Majorana 2 materials**: "The original Majorana superconductor used aluminum, but Majorana 2 uses lead, which is commonly used to shield people and equipment from radiation in hospitals and industrial settings"
6. **Majorana 2 reliability**: "qubits can maintain their quantum state 1,000 times longer than the first generation, enabling more reliable computation"
7. **Majorana 2 comparison**: "While other common approaches measure a qubit's 'lifetime' in microseconds, Majorana 2 offers a mean qubit lifetime of 20 seconds, with some instances lasting as long as one minute"

### 16. Microsoft Discovery — General Availability
**Products**: Microsoft Discovery, Microsoft Discovery app
**Blog**: https://aka.ms/AA10vjcq

1. **Microsoft Discovery GA**: "its comprehensive platform for organizations to embrace Frontier R&D. This combines specialized AI agents for scientific research and development, a Discovery Engine that drives research and reasoning workflows, plus enterprise-level security, governance and transparency"
2. **Microsoft Discovery app**: "core capabilities that individuals can download for free and run locally on their computers with a GitHub Copilot account, lowering the barrier to entry for advanced AI-driven research"
3. **Microsoft Discovery capabilities**: "allows researchers to deploy autonomous agent teams, guided by human expertise, that can reason over large amounts of knowledge, generate hypotheses, optimize experiments, validate theories and learn in a continuous loop"
4. **Customer stories**: "we've seen customers light up use cases across critical industries like life sciences, chemicals and materials, energy, manufacturing and consumer goods"
5. **Customer story — Syensqo**: "Syensqo developing next-generation fluids for semiconductor manufacturing"

### 17. Agentic AI for Quantum — Use Cases
**Products**: Microsoft Discovery, Majorana 2
**Blog**: https://aka.ms/AA10vjcq

1. **Agentic AI for materials**: "Microsoft Discovery is being used more extensively for future Majorana materials work"
2. **Agentic AI for fabrication**: "the team used it to help manage the manufacturing of the new device"
3. **Agentic AI for measurements**: "Using agentic capabilities available in Microsoft Discovery, the team was able to create an AI agent specialized for this job, which cut the cycle time by orders of magnitude"
4. **Agentic AI for data synthesis**: "As you run AI agents on this data, they're able to essentially resynthesize and make correlations that we as humans cannot see because no single individual has that much vision across that much data"
5. **Agentic AI for noise filtering**: "the team developed an AI agent that was able to combine physics, device and institutional knowledge to filter raw data from the quantum team's fabrication process and sniff out an uncalibrated temperature sensor reading that was throwing things off"

---

## Blog 3: HERO — Enterprise Agent Platform (Jay Parikh)

### 18. Microsoft Agent Platform — Architecture
**Products**: Azure, GitHub, Microsoft IQ, Fabric, Foundry, Windows, Microsoft Security, Microsoft 365, Agent 365
**Blog**: https://aka.ms/AA1188jd

1. **Single integrated system**: "we're bringing together Azure, GitHub, Microsoft IQ, Fabric, Foundry, Windows, Microsoft Security, and Microsoft 365 to operate as a single system you can use to deploy agents at enterprise scale"
2. **Platform principles — secured and governed**: "By extending Entra, Purview, Defender, Agent 365, and the broader Microsoft Security stack, governance becomes native to the system rather than bolted on later"
3. **Platform principles — continuous improvement**: "Agent behavior, outcomes, and human feedback must flow back into the system, so it can improve safely over time under human oversight"

### 19. Build in GitHub
**Products**: GitHub, GitHub Copilot
**Blog**: https://aka.ms/AA1188jd

1. **GitHub as agent build platform**: "Agents should be built the same way production software is built. You write code with GitHub Copilot to move faster"
2. **Agent lifecycle**: "Agents must follow a lifecycle: source, test, deploy, observe, and improve. GitHub sets up that lifecycle and provides the necessary controls from day one"
3. **New app**: "you can do all this in one place, in a new app built for this system"

### 20. Contextualize with Microsoft IQ
**Products**: Microsoft IQ, Web IQ, Frontier Tuning, MAI models
**Blog**: https://aka.ms/AA1188jd

1. **Microsoft IQ grounding**: "Microsoft IQ grounds agents in enterprise context by connecting to your business data wherever it lives, across Microsoft 365, your core business systems (such as customer and revenue data), and other systems your enterprise already relies on, like knowledge bases and your website"
2. **Web IQ**: "the latest addition to the IQ platform, agents can also incorporate relevant information from the web when appropriate"
3. **Microsoft IQ function**: "Microsoft IQ organizes, secures, and surfaces the right information in forms agents can actually use, so they can reach accurate insight without drowning in noise or hallucinating answers"
4. **Seven new MAI models**: "seven new MAI models, spanning image, voice, transcription, coding, and reasoning"
5. **Reinforcement learning environments**: "Our reinforcement learning environments allow our models to be reinforced through actual outcomes in your environment. Think of them as training gyms for AI"
6. **Frontier Tuning result**: "your custom or post-trained models all stay in your environment. Your intellectual property, your proprietary data, and the way work actually gets done become part of how your agents reason and act"

### 21. Run in Foundry
**Products**: Microsoft Foundry, Fireworks AI, Microsoft Agent Framework, GitHub Copilot SDK, Claude Agent SDK, LangGraph
**Blog**: https://aka.ms/AA1188jd

1. **Foundry as runtime**: "Foundry is the runtime designed for that reality"
2. **Model collection**: "Whatever the task, whatever the cost profile, Foundry provides access to the right model, and an optimized model router helps you balance quality, speed, and cost for each agent"
3. **Fireworks AI on Foundry**: "With Fireworks AI on Foundry, enterprises get faster, more efficient inference directly into the platform"
4. **Framework support**: "Bring in agents built on the Microsoft Agent Framework, LangGraph, GitHub Copilot SDK, Claude Agent SDK, or a custom harness"
5. **Evals and traces**: "Observability and traces make agent behavior measurable. If you can't measure it, you can't improve it"
6. **Continuous optimization**: "Foundry enables tuning of models, harnesses, IQs, tools, and actions over time, improving performance as agents operate in your world"

### 22. Govern with Agent 365
**Products**: Agent 365, Entra, Purview, Defender, MDASH
**Blog**: https://aka.ms/AA1188jd

1. **Agent 365 catalog**: "Every agent in your organization shows up in a single catalog, whether it was built in Foundry or elsewhere"
2. **Agent 365 visibility**: "IT sees who deployed an agent, what data and tools it can access, how it's behaving, and what it costs. They can enforce policy or take action when required"

### 23. Continuous Improvement Loop
**Products**: Microsoft Foundry
**Blog**: https://aka.ms/AA1188jd

1. **Improvement loop**: "Every agent action generates signal: trajectories, outcomes, feedback. The system captures it, refines it, and feeds it back. Observe. Evaluate. Improve. Roll out safely. Repeat"
2. **Improvement approach**: "Most gains start with eval-driven improvements to the agent itself: prompts, context, skills, and tools. As clear patterns emerge, learning can extend into model routing across multiple models, fine-tuning, or reinforcement learning"

### 24. Surface in Microsoft 365 and Scale on Azure
**Products**: Microsoft Teams, Microsoft 365, Windows, Azure
**Blog**: https://aka.ms/AA1188jd

1. **Agent surfacing**: "Agents surface directly in the flow of work, in Teams, across Microsoft 365, and inside your own applications and experiences"
2. **Windows for agents**: "your agents can be developed and run in an optimized and secure way on Windows. You can run models both in the cloud and locally on your machine, and best-in-class sandboxing lets you run always-on agents safely"

---

## Blog 4: HERO — Windows

### 25. Coreutils for Windows
**Products**: Coreutils for Windows
**Blog**: https://aka.ms/Windows-Build2026

1. **Coreutils for Windows**: "a set of Linux-like command line utilities that run natively on Windows, now generally available"
2. **Coreutils for Windows**: "built from the uutils open-source project, a cross-platform reimplementation of GNU Coreutils in Rust"
3. **Coreutils for Windows**: "Whether you're moving between Linux, macOS, WSL, containers or cloud environments, the commands and workflows you've built over years just work in your Windows environment"

### 26. WSL Containers
**Products**: WSL containers, WSL containers CLI, WSL containers API
**Blog**: https://aka.ms/Windows-Build2026

1. **WSL containers**: "a built-in way to create, run and interact with Linux containers using familiar CLI & API, coming soon to public preview"
2. **WSL containers CLI**: "Use the new exe binary to directly build, run and deploy Linux containers on Windows, out of the box"
3. **WSL containers API**: "Access functions to run Linux containers programmatically in your native Windows apps – unlocking scenarios like running local AI workloads, testing pipelines, and Linux based processing"
4. **WSL containers for enterprise**: "WSL containers provide policy‑based enablement and management using familiar Windows controls"

### 27. Windows Developer Configurations
**Products**: Windows Developer Configurations, WinGet
**Blog**: https://aka.ms/Windows-Build2026

1. **Windows Developer Configurations**: "powered by WinGet, sets up a distraction-free dev environment with VS Code, GitHub Copilot, WSL, PowerShell 7 and developer-optimized settings with one command on any Windows 11 device, now generally available"
2. **dev-config.winget**: "a WinGet configuration file, to get an optimized, distraction free development environment with the right versions of essential developer tools installed"

### 28. Intelligent Terminal
**Products**: Intelligent Terminal, ACP (Agent Communication Protocol)
**Blog**: https://aka.ms/Windows-Build2026

1. **Intelligent Terminal**: "intentionally brings context-aware intelligence to your favorite agents directly into a terminal based experience to help debug errors, run multi-step tasks so you can stay in your flow, available in experimental preview"
2. **Intelligent Terminal**: "provides context to your favorite agents via ACP (Agent Communication Protocol) so you can stay in the terminal and query, debug or complete any task on hand"
3. **Intelligent Terminal**: "based on the existing Windows Terminal experience, so you get everything it offers (tabs, profiles, themes, settings, shells) plus native agent CLI integration in the agent pane"
4. **Intelligent Terminal**: "when a command fails, Intelligent Terminal automatically surfaces the context and suggests fixes you can run immediately in the dedicated agent pane"

### 29. Windows Development Skills
**Products**: Windows Development Skills, WinUI3 skills, WinApp CLI
**Blog**: https://aka.ms/Windows-Build2026

1. **Windows Development Skills**: "gives agents structured knowledge to build great native Windows apps end-to-end using WinUI3 skills and WinApp CLI, now generally available"
2. **Windows Development Skills**: "enable agents to directly leverage structured knowledge to execute across the full lifecycle of building a native Windows app"

### 30. Windows 365 with Developer Configuration
**Products**: Windows 365
**Blog**: https://aka.ms/Windows-Build2026

1. **Windows 365 with Developer configuration**: "Windows 365 comes pre-configured with the same Windows developer configuration, available in public preview"
2. **Windows 365 with Developer configuration**: "offers ready‑to‑code environments in the cloud. This image provides a consistent, preconfigured Windows 11 development experience from first sign‑in"

### 31. Microsoft Execution Containers (MXC) SDK
**Products**: Microsoft Execution Containers (MXC), MXC SDK
**Blog**: https://aka.ms/Windows-Build2026

1. **MXC SDK**: "A policy-driven execution layer that lets developers declare what an agent can access (e.g., files, network) with containment boundaries enforced at runtime"
2. **MXC**: "offers a spectrum of isolation semantics that are dynamically composable based on intent and risk, available in early preview"
3. **MXC process isolation**: "Fast process isolation (adopted by GitHub Copilot CLI) and session isolation separates the agent's execution from the user's desktop, clipboard, UI and input devices"
4. **MXC session isolation**: "binds the agent to a strong user identity — mitigating UI spoofing, input injection and cross-session data leakage"
5. **MXC roadmap**: "Micro-VMs, Linux containers and MXC integration for Windows 365 for Agents are currently on our roadmap as additional MXC containment capabilities"

### 32. Agent 365 Native Integration with MXC
**Products**: Agent 365, Defender, Entra, Intune, Purview
**Blog**: https://aka.ms/Windows-Build2026

1. **Agent 365 native integration**: "enables agents running on Windows to start secure and stay secure. Integration will deliver Defender, Entra, Intune and Purview protections so security and IT teams can constrain and secure local agents to prevent enterprise risk, available in preview in July"
2. **OS-enforced Agent Identity**: "Windows assigns agents a local ID or a cloud provisioned identity backed by Entra and attributes all activity from the container to that identity, so you can clearly differentiate human from agent"

### 33. OpenClaw on Windows
**Products**: OpenClaw
**Blog**: https://aka.ms/Windows-Build2026

1. **OpenClaw on Windows**: "now runs the node and gateway securely on Windows leveraging MXC"
2. **OpenClaw on Windows**: "You can use the new Windows companion app to easily set up your own claws or connect to existing ones"

### 34. NVIDIA OpenShell on Windows
**Products**: NVIDIA OpenShell, MXC
**Blog**: https://aka.ms/Windows-Build2026

1. **NVIDIA OpenShell on Windows**: "Integrating MXC via OpenShell provides developers with an easy-to-deploy package for autonomous, always-on agents safely"

### 35. Partner Integrations — Hermes, Manus, OpenAI
**Products**: Hermes Agent, Manus, OpenAI Codex
**Blog**: https://aka.ms/Windows-Build2026

1. **Hermes Agent**: "will be integrating OpenShell and MXC in their new Windows application"
2. **Hermes Agent quote (Dillon Rolnick, CEO of Nous Research)**: "Microsoft Execution Containers (MXC), integrated with OpenShell, provides a policy-driven foundation for private, on-device agents on Windows"
3. **OpenAI quote (David Wiesen)**: "Working with Microsoft on the Microsoft Execution Containers (MXC) allows us to explore new patterns for AI agents to safely and efficiently generate and execute code"
4. **Manus quote (Tao Zhang, Chief Product Officer)**: "With Microsoft Execution Containers (MXC), Windows gives developers a policy-driven way to define what an agent can access and enforce those boundaries at runtime"

### 36. Windows 365 for Agents
**Products**: Windows 365 for Agents, Agent 365
**Blog**: https://aka.ms/Windows-Build2026

1. **Windows 365 for Agents**: "provides computer-using agents with secure, managed Cloud PCs to execute enterprise workflows, now generally available"
2. **Windows 365 for Agents**: "provides Cloud PCs that enable AI agents to execute multi-step workflows across software, including opening apps, navigating interfaces, entering inputs and processing data"

### 37. Aion 1.0 Instruct
**Products**: Aion 1.0 Instruct
**Blog**: https://aka.ms/Windows-Build2026

1. **Aion 1.0 Instruct**: "a smaller, faster and smarter on-device SLM"
2. **Aion 1.0 Instruct**: "our next-generation small language model, smaller, faster and more efficient than our current Windows OS SLM"
3. **Aion 1.0 Instruct**: "Designed from the ground up for on-device workloads, Aion 1.0 Instruct powers everyday text intelligence (summarization, rewrite, intents, accessibility) and extends beyond Windows APIs with integration into the Edge browser and availability as open weights"

### 38. Aion 1.0 Plan
**Products**: Aion 1.0 Plan
**Blog**: https://aka.ms/Windows-Build2026

1. **Aion 1.0 Plan**: "a reasoning and tool-calling model that enables fully local agentic capabilities, available in the coming months"
2. **Aion 1.0 Plan**: "a 14-billion parameter reasoning and tool-calling model with 32K context length that ships in-box as part of Windows on capable devices"
3. **Aion 1.0 Plan**: "enables applications to reason over user intent, invoke tools, manage files and orchestrate sub-agents, bringing fully agentic workflows onto the device"

### 39. Windows AI APIs Expansion
**Products**: Windows AI APIs, Speech Recognition API, Windows ML
**Blog**: https://aka.ms/Windows-Build2026

1. **Windows AI APIs expansion**: "Speech-to-text recognition API available on NPUs and CPUs. On-device SLM expands to capable dGPUs enabling text-intelligence capabilities locally and Video Super Resolution available on CPUs"
2. **Speech Recognition API**: "enables real-time or batch, on-device speech-to-text from live audio"
3. **Speech Recognition API**: "Developers can enable their apps to produce transcripts from recordings or embed captions anywhere audio plays, using microphone, streamed or audio file inputs, with hardware-accelerated execution where available"
4. **Windows AI APIs breadth**: "Windows AI APIs are expanding beyond NPUs to CPUs and GPUs, bringing local AI experiences to a much broader set of Windows 11 devices"

### 40. Surface RTX Spark Dev Box (Windows Blog)
**Products**: Surface RTX Spark Dev Box, NVIDIA RTX Spark
**Blog**: https://aka.ms/Windows-Build2026

1. **Surface RTX Spark Dev Box**: "purpose-built for developers powered by NVIDIA RTX Spark silicon, delivering up to 1 petaflop of AI compute paired with 128 GB of unified memory shared across the CPU and GPU"
2. **Surface RTX Spark Dev Box**: "ships with developer optimized Windows 11 experience – preconfigured with all your essential developer tools"
3. **Surface RTX Spark Dev Box**: "will be available later this year in the U.S. exclusively on Microsoft.com"

### 41. DGX Station for Windows
**Products**: DGX Station for Windows, NVIDIA GB300 Grace Blackwell Ultra Superchip
**Blog**: https://aka.ms/Windows-Build2026

1. **DGX Station for Windows**: "the world's most powerful deskside AI supercomputer for developing and running agents on Windows — powered by the NVIDIA GB300 Grace Blackwell Ultra Superchip"
2. **DGX Station for Windows**: "purpose-built to develop and run up to 1 trillion-parameter frontier AI models locally, as well as connect always-on, frontier AI agents to enterprise applications and workflows, coming in Q4 this year"

### 42. Project Solara
**Products**: Project Solara
**Blog**: https://aka.ms/Windows-Build2026

1. **Project Solara**: "a new platform built from the ground up to power agent-driven experiences, including two new concept devices that reimagine how this comes to life"

### 43. Microsoft Store Updates
**Products**: Microsoft Store
**Blog**: https://aka.ms/Windows-Build2026

1. **Microsoft Store**: "free and faster company onboarding with Entra ID support, accelerated app certification times, and new near real-time analytics and subscription insights for developers"

### 44. Windows Security Improvements
**Products**: Windows 11, Smart App Control, App Control for Business
**Blog**: https://aka.ms/Windows-Build2026

1. **Post-quantum cryptography**: "Windows continues to expand post-quantum cryptography (PQC) support across the platform, broadening algorithm coverage and integrating it more deeply into the platform"
2. **PQC specifics**: "PQ hybrid key exchange in the Windows TLS stack, support for composite PQC algorithms through Windows cryptography APIs (CNG) and certificate functions, and PQ certificate issuance via Active Directory Certificate Services (ADCS)"
3. **Legacy authentication**: "IAKerb and LocalKDC (in WIP Server and Client) are configurable via new registry keys, helping reduce NTLM usage and enable stronger Kerberos-based authentication across more scenarios"
4. **Driver signing**: "Driver signing now follows a higher security bar with an updated certification process"
5. **Smart App Control**: "Smart App Control for consumers and App Control for Business are expanding in coverage across millions of devices, with stronger reputation-based enforcement, new integration APIs and policy-driven control for enterprise environments"

### 45. GitHub Copilot CLI Local Task Delegation
**Products**: GitHub Copilot CLI
**Blog**: https://aka.ms/Windows-Build2026

1. **GitHub Copilot CLI /fleet**: "In GitHub Copilot CLI we will enable developers to configure selective task delegation to subagents powered by a local model. Using /fleet, the primary agent running in the cloud builds a plan, assesses the complexity of each task, and routes appropriate ones locally based on the models' size and capability"

---

## Blog 5: HERO — Microsoft AI (MAI Models)

### 46. MAI Model Family — Foundation
**Products**: MAI models, Microsoft Foundry, Open Router, Fireworks, Baseten
**Blog**: http://aka.ms/MAI-Build

1. **MAI distribution**: "our models are also going to be widely available for developers on Open Router, as well as Fireworks and Baseten"
2. **MAI weight tuning**: "For the first time developers will be able to tune the weights of the model themselves"
3. **MAI foundation**: "All these models are built on a shared foundation, hill-climbing from the bottom with zero distillation. They share the same data discipline, the same infrastructure and the same evaluation framework"

### 47. Frontier Tuning (MAI Blog)
**Products**: Frontier Tuning, MAI models
**Blog**: http://aka.ms/MAI-Build

1. **Frontier Tuning definition**: "With reinforcement learning in real-world environments, AI can fully adapt to the specifics of a given workflow for the first time. We call this Microsoft Frontier Tuning"
2. **Reinforcement learning environments**: "Our reinforcement learning environments (RLEs) allow your MAI models to learn directly from your workflows. Think of them as training gyms for AI, accessible only to you"
3. **Frontier Tuning ownership**: "With Frontier Tuning, you're building your own model, trained on your data, within your environment, controlled by you. Your institutional knowledge becomes part of the model, and it stays yours"
4. **Frontier Tuning — Excel benchmark**: "our MAI tuned model for Excel matches GPT 5.4 while being up to 10× more efficient"
5. **Frontier Tuning — McKinsey**: "When tuned for McKinsey's exacting enterprise standards, MAI achieved the highest win rate of any model tested at roughly 10× lower cost"

### 48. Mayo Clinic Collaboration
**Products**: Mayo Clinic frontier AI model, Azure Foundry
**Blog**: http://aka.ms/MAI-Build

1. **Mayo Clinic collaboration**: "Microsoft and Mayo Clinic are collaborating to co-create a frontier AI model for healthcare that brings together Mayo Clinic's world-leading clinical expertise, de-identified clinical data and longitudinal insights with Microsoft's foundational AI capabilities"
2. **Mayo Clinic model scope**: "This model will be designed to excel at the broadest scope of clinical reasoning and healthcare use cases, reaching a level that today's general-purpose systems simply cannot match"
3. **Mayo Clinic deployment**: "The model will first be deployed within Mayo Clinic's own environment, the world's top hospital system, where we expect it to enable a broad range of capabilities, including earlier and more accurate diagnoses and treatment planning"
4. **Mayo Clinic availability**: "Once validated, the model will be made available to other organizations via Azure Foundry, making Mayo Clinic's expertise accessible to many more who need it"
5. **Mayo Clinic ownership**: "The frontier AI model will be owned by Mayo Clinic"

### 49. MAI Lab — Infrastructure
**Products**: Maia 200, MAI
**Blog**: http://aka.ms/MAI-Build

1. **MAI training approach**: "We train from scratch. We don't distill from other labs and we don't rely on unlicensed or opaque data. Our datasets are clean and appropriately licensed"
2. **MAI infrastructure**: "Every component of the system, from architecture to training pipeline to post-training, we built ourselves"
3. **Maia 200 silicon**: "We co-design with our own Maia 200 silicon, and are already seeing a 1.4x efficiency boost from these efforts"
4. **MAI transparency**: "today we are publishing in depth safety and technical reports"

### 50. Humanist Superintelligence
**Products**: MAI
**Blog**: http://aka.ms/MAI-Build

1. **Humanist Superintelligence**: "Our ultimate goal is what we call Humanist Superintelligence. That means advanced AI systems designed to serve people and organizations, not replace them"
2. **Humanist Superintelligence principles**: "These systems must remain tools, shaped by human intent, accountable to human oversight, and ultimately subordinate to human goals"

---

## Summary Statistics

| Blog | URL | Status | Statement Count |
|------|-----|--------|----------------|
| 1. OMB Developer Blog | https://aka.ms/AA10pe80 | ✅ Full content | 38 |
| 2. HERO: Quantum + Discovery | https://aka.ms/AA10vjcq | ✅ Full content | 17 |
| 3. HERO: Enterprise Agent Platform | https://aka.ms/AA1188jd | ✅ Full content (NOT 404) | 22 |
| 4. HERO: Windows | https://aka.ms/Windows-Build2026 | ✅ Full content | 42 |
| 5. HERO: Microsoft AI | http://aka.ms/MAI-Build | ⚠️ Partial (JS-rendered, missing first half with model specs) | 15 |

**Total statements extracted: 134**

### Notes
- **Blog 3 (https://aka.ms/AA1188jd)**: Was expected to be 404 but is LIVE. This is the Jay Parikh enterprise agent platform blog.
- **Blog 5 (http://aka.ms/MAI-Build)**: The page at microsoft.ai renders model details via JavaScript. Only the second half of the blog was accessible (Frontier Tuning, Mayo Clinic, Lab, Humanist Superintelligence sections). The first half covering individual model specs (MAI-Thinking-1, MAI-Image-2.5, etc.) is JS-rendered and not extractable. However, detailed MAI model announcements are captured from Blog 1 (OMB) which contains the same information.
- The blog title from HTML metadata is: "Building a hill-climbing machine: Launching seven new MAI models"

---

# Batch 2: Live Blog Items — AI + Innovation + Mayo — Tier 3

## Build 2026 Announcements Index

---

### 1. Majorana 2 — Microsoft's Scalable Quantum Processor
**Products**: Majorana 2
**Blog**: https://aka.ms/m2blog

1. **Majorana 2 quantum processor with lead-based material stack**: "Majorana 2 contains qubits that are 1,000x more reliable than those in our previous quantum processing unit."
2. **New material stack replacing aluminum with lead**: "The new material stack, which swaps aluminum for lead, creates highly reliable topological qubits with operations on the microsecond scale and lifetimes with a mean of 20 seconds, occasionally exceeding one minute."
3. **Enhanced qubit lifetimes**: "In the aluminum-based Majorana 1, qubit lifetimes were between one and 12 milliseconds, whereas in Majorana 2, the lifetimes exceed 20 seconds, representing more than 1,000x improvement in stability."
4. **Accelerated roadmap to scalable quantum computer**: "We are accelerating our roadmap to a scalable, practical quantum computer—we have cut our timeline in half and now aim to reach this target by 2029."
5. **DARPA Quantum Benchmarking Initiative final phase**: "DARPA and Microsoft executed an agreement to begin the final phase of the program."

---

### 2. Microsoft Discovery — Enterprise Platform for Agentic AI in R&D
**Products**: Microsoft Discovery, Microsoft Discovery app, Microsoft Discovery Engine
**Blog**: https://aka.ms/MicrosoftDiscoveryBlog

1. **Microsoft Discovery generally available**: "Microsoft Discovery is now generally available for all organizations, providing a comprehensive platform for building and governing agentic AI workflows across scientific and engineering disciplines."
2. **Microsoft Discovery app in preview**: "We are also introducing the Microsoft Discovery app in preview, a local desktop experience that helps researchers, students, and scientific teams begin working with Microsoft Discovery today."
3. **Microsoft Discovery Engine**: "At the center of the platform is the Microsoft Discovery Engine, which supports the core loop of scientific work by helping teams move from evidence to hypotheses, through execution and analysis, and into the next iteration."
4. **Microsoft Discovery app available on GitHub**: "The Microsoft Discovery app is a localized experience that gives researchers, students, academic labs, and scientific teams a simpler way to begin using Microsoft Discovery capabilities without starting with a full enterprise deployment."

---

### 3. Microsoft Scout — First Autopilot Agent
**Products**: Microsoft Scout, Autopilots, OpenClaw, Work IQ
**Blog**: https://aka.ms/ProjectLobster-Blog

1. **New category of agents called Autopilots**: "Autopilots are always-on agents that work autonomously, with their own identity, and act on your behalf."
2. **Microsoft Scout introduction**: "Microsoft Scout is integrated across the Microsoft 365 apps you use every day, keeping it grounded in your flow of work."
3. **Powered by OpenClaw open-source technology**: "It is powered by OpenClaw open-source technology, reflecting our commitment to building with the community while extending capabilities to meet enterprise needs."
4. **Work IQ context building**: "Over time, Microsoft Scout builds context powered by Work IQ, learning how you work, what you care about, and what needs to happen next."
5. **Enterprise identity and governance**: "Every agent operates under its own governed Entra identity, not a shared, anonymous service account, so the work it does is attributable to a known actor your directory already understands."

---

### 4. Agent Control Specification (ACS) — Runtime Governance for AI Agents
**Products**: Agent Control Specification, Agent Governance Toolkit
**Blog**: https://commandline.microsoft.com/agent-control-specification-runtime-governance/

1. **Agent Control Specification (ACS) open specification**: "ACS is an open specification and reference implementation for the runtime governance layer of AI agents."
2. **Portable manifest for policy enforcement**: "Its core artifact is a portable manifest that defines where, when, and how policies are evaluated and enforced across the full agent lifecycle, independent of the agent framework, the runtime, or the policy engine that authors the rules themselves."
3. **Eight interception points**: "ACS defines eight interception points where policies can be evaluated against the agent's runtime context."
4. **Part of Agent Governance Toolkit**: "It's a new module within Microsoft's Agent Governance Toolkit (AGT), extending how developers manage and govern AI agents."

---

### 5. ASSERT — Specification-Driven Evaluation Framework
**Products**: ASSERT
**Blog**: https://commandline.microsoft.com/assert-written-intent-executable-evals/

1. **ASSERT open-source framework release**: "Today, we're releasing Adaptive Spec-driven Scoring for Evaluation and Regression Testing (ASSERT), an open-source framework for turning natural-language behavior specifications into executable evaluations."
2. **Behavior specification as first-class input**: "ASSERT is built on the premise that a behavior specification should be a first-class input to evaluation—not just the background context."
3. **Four-stage evaluation pipeline**: "The framework systematizes the specification, converts it into an inspectable taxonomy, generates stratified test cases from the taxonomy, runs the test cases against the target, and scores each failure against the policy statement that produced it."
4. **Validation results**: "Compared with a comparable in-house baseline, ASSERT covered roughly 1.2x as much of the intended behavior space, surfaced about 1.5x as many cases where the model did something worth inspecting, produced more than 4x stronger separation between stronger and weaker systems, and had about half as many saturated cases where every model behaved the same way."

---

### 6. Mayo Clinic and Microsoft — Frontier AI Model for Healthcare
**Products**: Mayo Clinic Platform, Azure Foundry APIs
**Blog**: https://news.microsoft.com/source/?p=24971

1. **Frontier AI model for healthcare**: "Mayo Clinic and Microsoft today announced a strategic collaboration to develop and deploy a frontier AI model designed specifically for healthcare, making Mayo Clinic's knowledge, expertise and integrated model of care available to more people when and where they need it."
2. **Model designed for clinical reasoning**: "The model is designed to synthesize diverse clinical data to support earlier diagnoses, more personalized treatment decisions and better patient outcomes."
3. **Model available through Azure Foundry APIs**: "Microsoft plans to make the model available through Azure Foundry APIs, enabling organizations worldwide to access advanced healthcare AI capabilities designed to better support patients, clinicians and consumers."
4. **Mayo Clinic owns the model**: "The frontier AI model will be owned by Mayo Clinic, reinforcing Mayo's longstanding commitment to patient trust, clinical rigor, safety and responsible stewardship of clinical data and AI."

---

# Batch 3: Live Blog Items — Azure (Tier 3)

## Microsoft Build 2026 Announcements Index

---

### 1. Azure Cobalt 200 Arm-based Virtual Machines
**Products**: Azure Cobalt 200 Arm-based Virtual Machines, Azure Boost
**Blog**: https://aka.ms/Cobalt200VMs

1. **Azure Cobalt 200 Arm-based Virtual Machines (early access preview)**: "We are announcing the early access preview for Azure Cobalt 200 Arm-based Virtual Machines (VMs), designed from the ground up for scale-out, cloud-native, and Linux-based agentic AI workloads, with up to 50% better generational performance over Cobalt 100."
2. **Up to 128 vCPUs**: "Cobalt 200 VMs scale up to 128 vCPUs, delivering more compute capacity for demanding scale-out, cloud-native, agentic AI, and data-intensive workloads."
3. **Stronger security by default**: "Memory encryption is enabled by default through a custom-designed memory controller, helping raise the baseline security posture for every workload with negligible performance impact."
4. **New VM families (Mpsv4 and Lpsv5)**: "Cobalt 200 adds two more VM families: the High-Memory Optimized Mpsv4 VMs and Dense Local Storage Lpsv5 VMs, bringing more choice across compute, memory, and storage profiles."

---

### 2. Azure HorizonDB
**Products**: Azure HorizonDB
**Blog**: https://aka.ms/HorizonDB-Build-blog

1. **Azure HorizonDB (public preview)**: "Azure HorizonDB, a new enterprise-ready Postgres-compatible database service designed to meet the needs of modern AI applications."
2. **DiskANN with spherical quantization**: "HorizonDB brings high-performance vector search directly into Postgres through DiskANN with spherical quantization."
3. **Integrated AI model management**: "HorizonDB introduces integrated AI model management to simplify how models are registered, versioned, and governed alongside data, including built-in support for generative GPT models and ranking models."
4. **AI Functions via azure_ai extension**: "These functions are implemented through the azure_ai extension, which brings model invocation directly into the Postgres engine."
5. **AI Pipelines**: "AI Pipelines operationalize these capabilities through reliable, event-driven workflows for model execution and data processing."

---

### 3. Web IQ
**Products**: Web IQ
**Blog**: https://aka.ms/nextgengrounding

1. **Web IQ launch**: "Microsoft is launching Web IQ: a suite of AI-native grounding APIs built for the agentic era, connecting AI systems and agents to fresh, real-world intelligence from across the web — including web pages, news, images, and videos."
2. **Re-architected grounding stack**: "Web IQ is a search engine for AI systems. Where Bing was built to help people search the web, Web IQ is built to help AI agents find the right information, turn it into useful evidence, and use it inside reasoning."
3. **Sub-165ms p95 latency**: "Web IQ is designed for production-scale speed, operating at sub-165ms p95 latency and, in our internal comparisons, nearly 2.5× faster than the next best alternative."
4. **Passage-level evidence**: "Web IQ does not just return documents; it returns passages and structured evidence objects."

---

### 4. Foundry IQ
**Products**: Foundry IQ, Foundry IQ Serverless, Foundry IQ MCP server
**Blog**: https://aka.ms/FoundryIQ

1. **Foundry IQ Serverless (public preview)**: "Provision instant, no-friction context retrieval with scale to zero pricing."
2. **Foundry IQ knowledge bases (generally available)**: "Ship production agents on a fully SLA-backed knowledge layer with stable APIs, compliance certifications, and the Foundry IQ MCP server for any MCP-compatible host."
3. **New knowledge sources (preview)**: "Ground agents across Work IQ, Fabric IQ (including Data agents and Ontology), File Search, Azure SQL, and MCP through a multi-source knowledge base, with no custom integrations required."
4. **Web IQ in Foundry IQ**: "Extend agent context to the web, honoring publisher preferences, and marketplace data with sub-165 ms latency and zero data retention."
5. **Agentic retrieval quality improvements**: "The latest updates to the agentic retrieval engine improve answer performance across datasets, effort tiers, and model sizes while spending fewer tokens."

---

### 5. Microsoft Fabric and Databases — Build 2026
**Products**: Microsoft Fabric, Rayfin, Azure HorizonDB, Azure Cosmos DB, Fabric Data Warehouse, Fabric IQ, OneLake
**Blog**: https://aka.ms/Azure-Data-Build26

1. **Rayfin (new open-source SDK and CLI)**: "Rayfin, a new open-source SDK and CLI, is designed to close that gap. It lets developers and coding agents describe what to build and get an enterprise-grade application backend directly into the application code, including a database, authentication, and more."
2. **GPU-accelerated Fabric Data Warehouse**: "We are introducing GPU-acceleration built directly into Fabric Data Warehouse to unlock a new level of performance without adding complexity."
3. **Fabric IQ (generally available)**: "Fabric IQ, now generally available, addresses this gap."
4. **General availability of graph and planning in Fabric**: "We're announcing the general availability of graph in Fabric, with general availability of the planning in Fabric coming later this month."
5. **Azure Cosmos DB Linux Emulator (generally available)**: "The Azure Cosmos DB Linux Emulator is now generally available, enabling developers to build, test, and validate applications locally across Linux, macOS, and Windows without a cloud dependency."

---

### 6. GPU-Accelerated Fabric Data Warehouse
**Products**: Fabric Data Warehouse, NVIDIA accelerated computing
**Blog**: https://aka.ms/GPUAcceleratedFabricDW

_Note: This URL redirects to the same blog as https://aka.ms/Azure-Data-Build26. Key GPU-specific announcements:_

1. **First fully managed data warehouse with GPU acceleration**: "This breakthrough establishes Fabric Data Warehouse as the first fully managed data warehouse to offer GPU acceleration."
2. **Up to 7x faster performance**: "The GPU-accelerated Fabric Data Warehouse delivered up to 7x faster performance relative to three comparable external vendors for reporting and application workloads at 64-user concurrency."
3. **ACM SIGMOD Best Industry Paper of 2026**: "The research behind this innovation was recently recognized by ACM SIGMOD as the 'Best Industry Paper of 2026.'"

---

### 7. Microsoft Foundry — Build 2026 Recap
**Products**: Microsoft Foundry, Microsoft Agent Framework, Foundry Toolkit for VS Code, Foundry Agent Service, Toolboxes in Foundry, Voice Live, Fireworks AI on Foundry, ASSERT, Agent Control Specification
**Blog**: https://aka.ms/FoundryBuildNews

1. **Hosted agents in Foundry Agent Service (expected GA early July 2026)**: "Hosted agents in Foundry Agent Service, expected to reach general availability by early July 2026, provide a managed runtime for production agents."
2. **Toolboxes in Foundry (public preview)**: "Toolboxes in Foundry, in public preview, gives your agent a single managed endpoint for every tool type."
3. **Foundry Toolkit for VS Code (generally available)**: "Foundry Toolkit for VS Code is now generally available."
4. **Voice Live (generally available)**: "Voice Live unifies speech recognition, text-to-speech, turn detection, interruption handling, avatars, and other real-time conversational features into a single API."
5. **ASSERT and Agent Control Specification (open source)**: "ASSERT is Microsoft's new framework for policy-driven agent evaluation" and "Agent Control Specification (ACS) is an open industry specification for placing deterministic safety and security controls at five checkpoints in an agent's lifecycle."

---

### 8. Rayfin
**Products**: Rayfin, Microsoft Fabric
**Blog**: https://aka.ms/rayfin

_Note: This URL resolves to a customer testimonial page, not a standalone blog post. The primary Rayfin announcement is covered in the Azure-Data-Build26 blog (Section 5 above)._

1. **Rayfin deploys to Microsoft Fabric**: "Rayfin then deploys directly to Microsoft Fabric, giving every application enterprise-grade security and scale from day one. Developers and AI agents can now move from prompt to production without managing infrastructure."

---

## Summary

- **Total statements**: 35
- **Sections**: 8
- **URLs that redirected to same content**: https://aka.ms/GPUAcceleratedFabricDW → same blog as https://aka.ms/Azure-Data-Build26
- **URLs with limited content**: https://aka.ms/rayfin resolved to a customer testimonial page (Leatherman quote), not a full blog post; Rayfin coverage sourced from the Azure-Data-Build26 blog instead.

---

# Build 2026 News Index — Batch 4: Live Blog Items — More for Devs + Windows (Tier 3)

---

### 1. Work IQ APIs
**Products**: Work IQ APIs, Microsoft 365 Copilot, Model Context Protocol (MCP), Copilot Credits
**Blog**: https://aka.ms/MBJ02yr26

1. **Work IQ APIs general availability**: "Today we are announcing that the Work IQ APIs will be generally available on June 16, 2026."
2. **Agent-optimized tool surface via MCP**: "For tool calling, Work IQ APIs collapses operations into just 10 generic tools with progressive disclosure through model context protocol (MCP), so developers do not need to teach agents hundreds of data-specific tools."
3. **Token efficiency**: "The Work IQ APIs reduce the total number of tokens needed to retrieve context and use tools by moving more of the AI processing into the Work IQ runtime."
4. **Context API**: "The Context API aggregates the content that Copilot would use to respond to a query but instead of synthesizing it into a response, it returns the context in a format designed for agent consumption."
5. **Workspaces for agent state**: "Work IQ digital workspaces are within the Microsoft 365 tenant boundary, and store data, files, memory, progress, and intermediate outputs as agents reason through work."

---

### 2. GitHub Copilot App
**Products**: GitHub Copilot app, GitHub Copilot SDK, Copilot CLI, Copilot code review
**Blog**: https://github.blog/news-insights/product-news/github-copilot-app-the-agent-native-desktop-experience/

1. **GitHub Copilot app technical preview**: "The new GitHub Copilot app is the agent-native desktop experience built on GitHub. From a single My Work view, you can see work in motion across connected repositories: active sessions, issues, pull requests, and background automations."
2. **Canvases**: "Canvases are bidirectional work surfaces for humans and agents. A canvas might show a plan, pull request, browser session, terminal, deployment, dashboard, or workflow state."
3. **Cloud and local sandboxes**: "Cloud and local sandboxes for GitHub Copilot give agents a bounded place to act. Choose where Copilot runs—on your local machine or in the cloud—and begin unlocking agent-driven workflows while prioritizing security and enterprise policy enforcement."
4. **GitHub Copilot SDK generally available**: "Now generally available in Node.js/TypeScript, Python, Go, .NET, Rust, and Java, it exposes the same agentic runtime that powers the Copilot app."
5. **Copilot code review medium tier**: "Copilot code review now offers medium tier review, which routes pull requests to a higher-reasoning model for better precision and recall."

---

### 3. Frontier Tuning
**Products**: Frontier Tuning, Microsoft Copilot Studio, Microsoft Foundry, Reinforcement Learning Environment (RLE)
**Blog**: https://aka.ms/frontiertuningblog

1. **Frontier Tuning private preview**: "Today at Microsoft Build, we introduced Frontier Tuning, a new approach to making AI work the way your business does by applying reinforcement learning inside your compliance boundary with your own data, processes, and conventions."
2. **Reinforcement Learning Environment**: "Tuning runs in a managed Reinforcement Learning Environment (RLE) used both for post-training and inference."
3. **Copilot Studio and Foundry integration**: "We're announcing private preview, available through Forward Deployed Engineers, and upcoming availability in Microsoft Copilot Studio and Microsoft Foundry."
4. **Tuned outputs within compliance boundary**: "This system produces tuned models, embeddings, skills, orchestration logic, and a runtime harness. All of this runs on your data, with your controls, without leaving your compliance boundary."

---

### 4. Surface RTX Spark Dev Box
**Products**: Surface RTX Spark Dev Box, Surface Laptop Ultra, NVIDIA RTX Spark, AI Toolkit for VS Code, Windows ML, Microsoft Foundry
**Blog**: https://blogs.windows.com/devices/?p=263819

1. **Surface RTX Spark Dev Box introduction**: "Today at Microsoft Build, we are introducing Surface RTX Spark Dev Box, a compact developer PC engineered with NVIDIA RTX Spark superchip and built on the Windows developer platform, designed for local-first AI development."
2. **1 petaflop AI compute with 128 GB unified memory**: "At the heart of this new developer machine is the NVIDIA RTX Spark superchip, combining a powerful NVIDIA Blackwell RTX GPU and an ultra-efficient NVIDIA Grace CPU to deliver up to 1 petaflop of AI compute with 128 GB of unified memory."
3. **Run 120B+ parameter models locally**: "That's enough compute power to run 120B+ parameter models with 1 million token context locally at interactive speeds or fine-tune models that previously required cloud GPU instances."
4. **Developer-configured Windows 11 Pro image**: "Surface RTX Spark Dev Box ships with Windows 11 Pro pre-configured for developers at the image level."
5. **WSL 2 with GPU passthrough**: "Under the hood, WSL 2 is configured with GPU passthrough and CUDA support."

---

### 5. Windows 365 at Build 2026
**Products**: Windows 365, Windows 365 for Agents, Windows 365 Flex, Microsoft Dev Box, Microsoft Copilot Studio
**Blog**: https://aka.ms/W365Build26Blog

1. **Windows 365 for Agents generally available**: "Windows 365 for Agents is now generally available. Agent makers can use it as part of Agent 365 tools or through Microsoft Copilot Studio (preview). It enables enterprise AI automation by providing agents with secured, managed, and available Cloud PCs that run within real business environments."
2. **Windows 11 developer configuration image public preview**: "Windows 365 now supports Windows 11 developer configuration image, in public preview: It delivers a preconfigured, ready-to-code environment with tools developers already use, including Visual Studio Code, Git, GitHub CLI, Python, Node.js, and Windows Subsystem for Linux (WSL), available from first sign-in."
3. **Microsoft Dev Box in maintenance mode**: "With Microsoft Dev Box now in maintenance mode, Windows 365 is the forward-looking path at Microsoft for teams seeking to standardize developer environments on Cloud PCs."
4. **32vCPU and GPU Select plans**: "32vCPU Windows 365 Cloud PCs are now available in Windows 365 Enterprise and Windows 365 Flex, supporting compute-intensive workloads like software development, data modeling, simulations, and AI/ML."

---

### 6. Project Solara
**Products**: Project Solara
**Blog**: https://aka.ms/ProjectSolaraBuild2026

> ⚠️ **Unable to index**: This URL returned a sign-in page. Content was not publicly accessible at time of fetch.

---

*Generated: 2026-06-03*
*Source: Microsoft Build 2026 official blogs*

---

# Batch 5: Post-Keynote — AI + Innovation — Tier 3

---

### 1. Responsible AI for Agents — ASSERT and Agent Control Specification
**Products**: ASSERT, Agent Control Specification (ACS), Microsoft Foundry, Guided Guardrail Setup, Rubric evaluator
**Blog**: https://aka.ms/BuildFoundryRAI

1. **ASSERT (Adaptive Spec-driven Scoring for Evaluation and Regression Testing)**: "Microsoft's open-source framework for policy-driven agent evaluation, built on a proven Microsoft Research approach."
2. **Agent Control Specification (ACS)**: "An open industry specification for placing deterministic safety and security controls at checkpoints throughout agentic workflows, and it is part of the Agent Governance Toolkit."
3. **Guided Guardrail Setup in Foundry**: "Now in public preview, gives developers personalized guardrail recommendations in minutes."
4. **Rubric evaluator**: "Now in public preview, is a new evaluator in Microsoft Foundry that automatically generates evaluation criteria based on your agent's specific context."
5. **Runtime Data Loss Prevention (DLP) for agent prompts in Foundry**: "Purview introduces runtime data loss prevention (DLP) for agent prompts in Foundry, in preview with Agent 365. This capability detects, blocks, and audits sensitive data before it is processed by the agent, ensuring that sensitive information never reaches AI models."

---

### 2. Microsoft Security at Build 2026
**Products**: Microsoft Security multi-model agentic scanning harness (codename MDASH), Microsoft Defender, GitHub Code Security, Agent 365 SDK, Microsoft Execution Container (MXC), Windows 365 for Agents, Defender AI model scanning
**Blog**: https://aka.ms/BUILD_SecurityBlog

1. **Microsoft Security multi-model agentic scanning harness (codename MDASH)**: "This new agentic security system orchestrates a pipeline of more than 100 specialized AI agents using an ensemble of models to discover, validate, and prove exploitability across codebases written in popular programming languages."
2. **Integration between Microsoft Defender and GitHub Code Security**: "the integration between Microsoft Defender and GitHub Code Security (part of the former GitHub Advanced Security suite), now generally available, brings runtime context into development and security workflows so that teams can prioritize and address risks early minimizing the impact to human resources."
3. **Agent 365 SDK**: "With the general availability of the Agent 365 SDK, developers can integrate controls directly into their development workflows, bringing observability, access controls, and compliance enforcement into how agents are designed and deployed. This enables teams to build custom agents for any AI platform that are compliant, and enterprise-ready, and compose well with Agent 365."
4. **Windows 365 for Agents**: "Windows 365 for Agents, now generally available, enables you to run any agent in a fully isolated, policy-governed Cloud PC."
5. **Defender AI model scanning**: "Now developers can inspect model artifacts, whether platform-native or bring-your-own, with Defender AI model scanning, in preview. To help close gaps early model Defender AI model scanning detects and blocks potentially vulnerable or compromised models across registries, workspaces, and CI/CD pipelines to verify model integrity before deployment."

---

### 3. Microsoft Foundry Build 2026 Recap
**Products**: Microsoft Foundry, Foundry Toolkit for VS Code, Hosted agents, Toolboxes in Foundry, Voice Live, Memory in Foundry Agent Service, Fireworks AI on Foundry, MAI models
**Blog**: http://aka.ms/FoundryBuildNews
**Note**: Also appears in Batch 3 — will be deduplicated during merge.

1. **Hosted agents in Foundry Agent Service**: "Expected to reach general availability by early July 2026, provide a managed runtime for production agents."
2. **Foundry Toolkit for VS Code**: "Now generally available. Use it to create agents from templates or with GitHub Copilot, debug runs locally with trace visualization, connect to Toolboxes, and deploy to Foundry Agent Service from VS Code."
3. **Toolboxes in Foundry**: "In public preview, gives your agent a single managed endpoint for every tool type."
4. **Procedural memory**: "Helps agents learn how to do the work across runs, not just what was said. Early Tau-bench results show +7–14% absolute success-rate gains at near-baseline cost."
5. **Fireworks AI on Foundry**: "Now generally available, bringing open-model inference through a single Azure endpoint with enterprise SLAs, zero-setup onboarding, no separate infrastructure, and no separate contracts."

---

### 4. Foundry IQ — Governance and Enterprise AI Security
**Products**: Foundry IQ, Microsoft Purview, Azure AI Search
**Blog**: https://aka.ms/FoundryIQ-security

1. **Incremental SharePoint permissions sync**: "Incremental document ACL updates can be captured during scheduled indexer runs, including when scheduling is configured through Foundry IQ knowledge source settings for agentic retrieval."
2. **Purview sensitivity labels in Foundry IQ knowledge bases**: "Labels can flow from source systems into the index, through knowledge bases, and into the Foundry Agent experiences that depend on those knowledge bases."
3. **Elevated developer access with Purview auditing**: "This release introduces elevated read access for authorized developers and administrators, paired with auditing through Microsoft Purview."
4. **User-assigned managed identities for indexer pipelines**: "Now generally available. This enables identity-based authentication for data sources, knowledge stores, and encryption scenarios."

---

### 5. Foundry IQ — Richer Content Extraction and Data Enrichment
**Products**: Foundry IQ, Azure AI Search, Content Understanding in Foundry Tools
**Blog**: https://aka.ms/foundryIQ-data

1. **SharePoint indexer updates**: "The SharePoint indexer adds support for modern ASPX site pages and SharePoint Lists, in addition to document libraries."
2. **Content Understanding in Foundry Tools**: "Foundry IQ now supports semantic chunking and AI-generated image descriptions in preview with its Content Understanding in Foundry Tools data processing integration."
3. **Image serving for agentic retrieval**: "Image serving preserves extracted images during ingestion and makes them available at retrieval time. This allows models to reason over visual content alongside text."

---

### 6. Foundry IQ — Knowledge Bases Evaluation Results
**Products**: Foundry IQ knowledge bases, Azure AI Search
**Blog**: https://aka.ms/FoundryIQ-evals

1. **Knowledge bases improve evidence recall by up to 54%**: "Combining a smaller agent model with agentic retrieval improves evidence recall by up to 54% while controlling costs and increasing agent responsiveness."
2. **Agentic retrieval quality improvements**: "Since our last agentic retrieval release, we've made improvements in evidence recall as measured on multilingual enterprise content across all retrieval reasoning effort levels: 10% in minimal, 8% in low, and 9% in medium."
3. **Improved MCP schemas for Agentic Retrieval**: "Instead of serving a single fixed schema, the knowledge base dynamically specializes the schema for the orchestrating model's size and retrieval settings."

---

### 7. Kevin Scott — Build 2026 Lectures on Tap
**Products**: N/A (thought leadership)
**Blog**: https://commandline.microsoft.com/kevin-scott-build-2026-lectures-on-tap/

1. **Capability overhang**: "Today's AI models are actually more capable than the things we're using them for in the real world."
2. **Software velocity ≠ organizational velocity**: "In many cases, speeding up code generation simply exposes the slower-moving bottlenecks that were already present: deployment, integration, governance, and organizational change."
3. **Autonomy ≠ trust**: "You have to build systems doing complex things in a way where people can trust that they're doing them correctly and in a way that's aligned with their interests and values."

---

## URLs That Failed or Returned Irrelevant Content

| # | URL | Status |
|---|-----|--------|
| 1 | https://azure.microsoft.com/en-us/solutions/discovery | Returned product landing page, not a Build 2026 blog post |
| 2 | https://aka.ms/m2-paper | Returned Microsoft Quantum homepage, not a Build 2026 blog |
| 5 | https://aka.ms/build-observability | Returned login wall ("Sign in") |
| 7 | https://aka.ms/MarketplaceBuildBlog2026 | HTTP 404 |
| 8 | https://www.microsoft.com/insidetrack/blog/microsoft-build-2026:-empowering-our-developers-to-adopt-agentic-ai-at-microsoft/ | HTTP 404 |
| 9 | https://aka.ms/mfs-program-updates | HTTP 404 |
| 13 | https://aka.ms/GroundingAPIBuild2026/ | Returned login wall ("Sign in") |

---

# Batch 6: Post-Keynote — Azure — Tier 3

## Successfully Processed URLs

---

### 1. Microsoft Foundry — Models and Model Operations
**Products**: Microsoft Foundry, Fireworks AI on Microsoft Foundry, Model Router
**Blog**: https://aka.ms/BuildFoundryModels

1. **Fireworks AI on Microsoft Foundry**: "Fireworks AI on Microsoft Foundry is now generally available, giving developers access to production-grade open model inference through a single Azure endpoint, with enterprise service-level agreements (SLAs) and zero-setup onboarding."
2. **Model Router in Foundry Models**: "Model Router automatically routes each request to the most appropriate model based on workload characteristics, cost targets, and latency requirements."
3. **Model-agnostic platform**: "Microsoft Foundry is a unified platform to select, evaluate, optimize, operate, and continuously improve AI applications at production scale."
4. **Quota management**: "Scale more predictably with quota tiering, global customer quota, and data zone customer quota."

---

### 2. Microsoft Agent Platform — Foundry Agents
**Products**: Microsoft Agent Platform, Microsoft Agent Framework, Foundry Agent Service, Toolboxes in Foundry, Foundry IQ, Voice Live, Foundry Toolkit for VS Code
**Blog**: https://aka.ms/BuildFoundryAgents

1. **Microsoft Agent Framework**: "Microsoft Agent Framework is our opinionated, open-source agent framework, stable across Python and .NET. It unifies the enterprise foundations of Semantic Kernel with the multi-agent orchestration of AutoGen, so you no longer need to choose between them."
2. **Toolboxes in Foundry (public preview)**: "Toolboxes in Foundry gives your agent a single managed endpoint for every tool type. Configure tools once, point any MCP client at one URL, and let Foundry handle auth, lifecycle, and governance."
3. **Foundry IQ (generally available)**: "Foundry IQ is now generally available as the dedicated knowledge layer behind Foundry agents, unifying Work IQ, Fabric IQ, Azure SQL, File Search, and MCP sources behind one SLA-backed retrieval endpoint, with a Serverless tier in public preview and Web IQ for sub-200ms live web grounding."
4. **Hosted agents in Foundry Agent Service**: "Hosted agents in Foundry Agent Service (reaching general availability in the next 30 days) is the managed runtime for production agents. Every session runs in its own sandbox, isolating every agent execution with dedicated compute, memory and filesystem."
5. **Autopilot agents (public preview)**: "These agents act independently with Entra Agent ID, email address, Microsoft Teams presence, and place in the org chart. They can initiate conversations, work on shared files, follow up on action items, and collaborate with humans over time."

---

### 3. Microsoft Fabric and Microsoft Databases — Data Platform for AI
**Products**: Rayfin, Azure HorizonDB, Microsoft Fabric, Fabric IQ, Azure Cosmos DB, OneLake, Fabric Data Warehouse
**Blog**: https://aka.ms/Azure-Data-Build26
**Note**: Also appears in Batch 3. Will be deduplicated during merge.

1. **Rayfin**: "Rayfin, a new open-source SDK and CLI, is designed to close that gap. It lets developers and coding agents describe what to build and get an enterprise-grade application backend directly into the application code, including a database, authentication, and more."
2. **Azure HorizonDB (public preview)**: "Azure HorizonDB is a fully managed, PostgreSQL‑compatible database that combines PostgreSQL familiarity with cloud‑scale architecture. It's zone resilient by default and delivers elastic storage that scales to 128 TB, massive scale‑out compute up to 3,072 vCores, and can sustain sub‑millisecond, multi‑zone commit latency for demanding transactional scenarios."
3. **Fabric IQ (generally available)**: "Fabric IQ, now generally available, addresses this gap" — providing "a shared layer of business context" so "every agent starts with the same understanding of the business."
4. **GPU-accelerated Fabric Data Warehouse**: "We are introducing GPU-acceleration built directly into Fabric Data Warehouse to unlock a new level of performance without adding complexity." "This breakthrough establishes Fabric Data Warehouse as the first fully managed data warehouse to offer GPU acceleration."
5. **Operations agents (generally available)**: "Operations agents are now generally available. These agents are designed to continuously monitor real-time data, detect patterns or anomalies, and act based on predefined business logic."

---

---

## URLs That Failed to Load or Returned Irrelevant Content

| # | URL | Status |
|---|-----|--------|
| 2 | https://aka.ms/build26/CosmosDBAgents | **404 Not Found** |
| 5 | https://aka.ms/VMSSFlex-OS-Image-Upgrades-Preview | **Behind auth wall** (redirected to Microsoft sign-in) |
| 6 | https://aka.ms/Guest-RDMA-preview-blog | **Behind auth wall** (redirected to Microsoft sign-in) |
| 8 | https://aka.ms/azurefilesmacos | **Not a Build 2026 announcement** — documentation page on mounting Azure file shares on macOS |
| 9 | https://aka.ms/apim/build | **Behind auth wall** (redirected to Microsoft sign-in) |
| 10 | https://aka.ms/build/functions | **Behind auth wall** (redirected to Microsoft sign-in; target appears to be "Azure Functions at Build 2026 Update") |
| 11 | https://aka.ms/la/build | **Behind auth wall** (redirected to Microsoft sign-in) |

---

# Batch 7: Post-Keynote — More for Developers, Part 1 (Tier 3)

## Summary
- **URLs processed:** 10
- **Successfully extracted:** 3 (URLs 1+2 are the same blog)
- **Failed / inaccessible:** 7

---

### 1. Azure Linux 4.0 and Azure Container Linux
**Products**: Azure Linux 4.0, Azure Container Linux
**Blog**: https://aka.ms/azurecontainerlinux-blog

1. **Azure Linux 4.0 public preview on Azure Virtual Machines**: "the upcoming public preview of Azure Linux 4.0 on Azure Virtual Machines"
2. **General availability of Azure Container Linux**: "the general availability of Azure Container Linux, our immutable container-optimized operating system (OS)"
3. **Hardened Linux for cloud native and AI workloads**: "Together, they give developers and organizations a hardened Linux distribution purpose-built for cloud native and AI workloads."
4. **Agentic AI Foundation (AAIF)**: "The Agentic AI Foundation (AAIF) is already the fastest-growing project in Linux Foundation history."
5. **Microsoft Agent Framework**: "Our open source SDK and runtime for building, deploying, and managing multi-agent systems."

---

### 2. Azure HorizonDB: Enterprise-Ready Postgres, Engineered for the AI Era
**Products**: Azure HorizonDB, Visual Studio Code extension for PostgreSQL
**Blog**: https://aka.ms/build2026-postgres-releases

1. **Azure HorizonDB public preview**: "Today at Microsoft Build, we're pleased to announce the public preview of Azure HorizonDB, a new enterprise-ready Postgres-compatible database service designed to meet the needs of modern AI applications."
2. **DiskANN with spherical quantization**: "HorizonDB brings high-performance vector search directly into Postgres through DiskANN with spherical quantization."
3. **AI Functions via azure_ai extension**: "These functions are implemented through the azure_ai extension, which brings model invocation directly into the Postgres engine."
4. **AI Pipelines**: "AI Pipelines operationalize these capabilities through reliable, event-driven workflows for model execution and data processing."
5. **Integrated AI model management**: "HorizonDB introduces integrated AI model management to simplify how models are registered, versioned, and governed alongside data, including built-in support for generative GPT models and ranking models."

---

# Batch 8: Post-Keynote — More for Developers, part 2 + Windows — Tier 3

## Summary
- **URLs processed**: 11
- **URLs with extractable content**: 4
- **URLs failed/inaccessible**: 7 (see notes at bottom)

---

### 1. Azure Cobalt 200 Arm-based Virtual Machines
**Products**: Azure Cobalt 200 Arm-based Virtual Machines, Azure Boost, Azure Kubernetes Service (AKS)
**Blog**: https://aka.ms/Cobalt200VMs
**NOTE**: Also appears in Batch 3 — deduplicate during merge.

1. **Azure Cobalt 200 Arm-based Virtual Machines (early access preview)**: "We are announcing the early access preview for Azure Cobalt 200 Arm-based Virtual Machines (VMs), designed from the ground up for scale-out, cloud-native, and Linux-based agentic AI workloads, with up to 50% better generational performance over Cobalt 100."
2. **Up to 128 vCPUs**: "Cobalt 200 VMs scale up to 128 vCPUs, delivering more compute capacity for demanding scale-out, cloud-native, agentic AI, and data-intensive workloads."
3. **Stronger security by default**: "Memory encryption is enabled by default through a custom-designed memory controller, helping raise the baseline security posture for every workload with negligible performance impact."
4. **New VM families (Mpsv4 and Lpsv5)**: "Cobalt 200 adds two more VM families: the High-Memory Optimized Mpsv4 VMs and Dense Local Storage Lpsv5 VMs, bringing more choice across compute, memory, and storage profiles."
5. **Performance for agentic AI workloads**: "Cobalt 200 delivers the per-core performance and scalability needed to power modern agentic AI workloads."

---

### 2. Azure SRE Agent at Microsoft Build 2026
**Products**: Azure SRE Agent
**Blog**: https://aka.ms/Build26/blog/AppService (resolved: https://techcommunity.microsoft.com/blog/appsonazureblog/azure-sre-agent-at-microsoft-build-2026-bringing-agentic-operations-to-the-enter/4524669)

1. **VNet integration (Preview)**: "Run SRE Agent inside your private Azure workloads, with full support for enterprise network boundaries and private connectivity."
2. **Managed Connectors**: "A redesigned connector experience for governing, securing and scaling connections across observability, incident management, code, and collaboration tools plus an expanded SaaS connector catalog including Jira, GitLab, Slack, Power BI, and more."
3. **Private Plugins Marketplace**: "Give platform teams a governed way to publish approved skills, MCP tools, and operational workflows to every SRE Agent in the tenant."
4. **Native GitHub Enterprise support**: "Ground investigations in your enterprise repositories and workflows, so an incident can become an issue, an investigation, a pull request, and a repair plan — all under a governed service identity."

---

### 3. Azure Functions MCP extension — MCP Prompts
**Products**: Azure Functions MCP extension
**Blog**: https://aka.ms/Build26/blog/AppService (resolved: https://techcommunity.microsoft.com/blog/appsonazureblog/azure-functions-mcp-extension-now-supports-mcp-prompts/4516359)

1. **MCP prompt trigger (public preview)**: "The MCP prompt trigger is now available in public preview in the Azure Functions MCP extension!"
2. **All three core MCP server primitives**: "With this release, the extension now supports all three core MCP server primitives - tools, resources, and prompts, giving you a complete platform for building rich MCP servers on Azure Functions."
3. **MCP resource trigger (generally available)**: "The MCP resource trigger is generally available for serving resources and building interactive UIs in MCP Apps."

---

### 4. Making Windows the trustworthy OS for agents
**Products**: Microsoft Execution Containers (MXC) SDK, Windows, Agent 365, Windows 365 for Agents
**Blog**: https://blogs.windows.com/windowsdeveloper/?p=57808

1. **Microsoft Execution Containers (MXC) SDK (early preview)**: "We're introducing an early preview of the Microsoft Execution Containers (MXC) SDK, a cross-platform, policy-driven execution layer for agents on Windows and WSL."
2. **Process isolation for agents**: "Windows is simplifying how developers enable process isolation for agents. Process isolation provides fast, lightweight containment within the user's environment for scenarios like running model-generated code within a dedicated process boundary that restricts access to files and network domains outside defined policy."
3. **Session isolation**: "Sessions in Windows separate the agent's execution from the human user's environment, such as the interactive desktop, clipboard, UI, input devices and active sessions."
4. **GitHub Copilot CLI adopts MXC**: "GitHub Copilot CLI has adopted MXC process isolation to constrain what dynamically generated and executed code can do."
5. **Windows 365 for Agents (generally available)**: "Windows 365 for Agents, now generally available, extends containment beyond the local device."

---

## Failed/Inaccessible URLs

| # | URL | Issue |
|---|-----|-------|
| 2 | https://aka.ms/Lasv5-Laosv5-Pr | Redirected to Azure Compute blog listing page (no specific blog post) |
| 4 | https://aka.ms/AzureBackupCosmosDBpreviewTechBlog | Redirected to Microsoft sign-in page (auth-gated) |
| 5 | https://aka.ms/aca/build | Redirected to Microsoft sign-in page (auth-gated); target: "What's New in Azure Container Apps at Build26" |
| 6 | https://aka.ms/aca/sandboxes | Returned Azure Container Apps general landing/docs page (not a blog post) |
| 7 | https://aka.ms/InfrastructureResiliencyManager-PublicPreview-Blog | Redirected to Reliability and Resiliency blog listing page (no specific blog post) |
| 8 | https://aka.ms/build26/cosmosreranker | HTTP 404 — page not found |
| 9 | https://aka.ms/aks/build26 | Redirected to Tech Community home page (no specific blog post) |
| 10 | https://aka.ms/FL_Build_2026 | Redirected to Microsoft sign-in page (auth-gated) |

---

# Microsoft Build 2026 — Announcement Index (Newly Live URLs)

---

### 1. Agentic AI at Microsoft — Internal Developer Enablement
**Products**: Work IQ, Agent 365, Microsoft Copilot Studio, Azure DevOps, Model Context Protocol
**Blog**: https://www.microsoft.com/insidetrack/blog/microsoft-build-2026:-empowering-our-developers-to-adopt-agentic-ai-at-microsoft/

1. **Work IQ**: "How Work IQ is supercharging our AI usage at Microsoft"
2. **Agent 365**: "Deploying Microsoft Agent 365: How we're extending our infrastructure to manage agents at Microsoft"
3. **Model Context Protocol security and governance**: "Protecting AI conversations at Microsoft with Model Context Protocol security and governance"
4. **Microsoft Copilot Studio extensibility**: "Unlocking enterprise AI extensibility at Microsoft with Microsoft Copilot Studio"

---

### 2. Microsoft for Startups — Program Updates
**Products**: Microsoft for Startups, Microsoft Azure, Microsoft Foundry, Microsoft Marketplace
**Blog**: https://aka.ms/mfs-program-updates

1. **One path into Microsoft for Startups**: "Startups can apply directly through our website and start building immediately with access to Startup credits, Azure services, and AI capabilities through Microsoft Foundry."
2. **Startup credits that grow with your business**: "Qualified startups can start building immediately with Startup credits and access up to $150,000 over time based on service adoption and sustained usage on Azure."
3. **Expanding support for startups building on Azure**: "Eligible startups may now receive a dedicated Microsoft for Startups point of contact to help navigate benefits, technical resources, Microsoft Marketplace readiness, and co-sell opportunities."
4. **Helping startups reduce procurement friction**: "Through Marketplace and co-sell opportunities, startups can reduce procurement friction by selling through customers' existing Azure budgets."

---

### 3. Agentic Modernization — Closing the AI-readiness gap
**Products**: Azure Copilot migration agent, GitHub Copilot modernization agent
**Blog**: https://techcommunity.microsoft.com/blog/appsonazureblog/closing-the-ai-readiness-gap-with-agentic-modernization/4524011

1. **Azure Copilot migration agent (public preview)**: "Azure Copilot migration agent brings AI to every step of estate modernization planning - from discovery and assessment to dependency mapping, ROI analysis, and wave planning - reducing months of manual analysis to minutes."
2. **GitHub Copilot modernization agent (generally available)**: "GitHub Copilot modernization agent, now generally available, empowers application owners, architects, and developers to scale modernization across their entire application portfolio."
3. **Custom skills for the modernization agent (GA)**: "Custom skills let developers teach the modernization agent how their organization works by encoding proprietary patterns, libraries, Azure best practices, and migration approaches once, then reusing them across every run."
4. **First agentic end-to-end modernization solution**: "Azure Copilot migration agent and GitHub Copilot modernization agent create the first agentic, end-to-end modernization solution that unifies IT and developer workflows."

---

### 4. Physical AI — Small Form Factor Infrastructure
**Products**: Azure Local, Foundry Local, Azure Kubernetes Service, Azure IoT Operations, Provisioned Machine
**Blog**: https://techcommunity.microsoft.com/blog/azurearcblog/embed-intelligence-into-physical-systems-with-smaller-form-factor-infrastructure/4524876

1. **Lightweight deployments on smaller form factor hardware (preview)**: "We're extending Azure-based provisioning and management to smaller hardware form factors, using a lightweight, performance-oriented architecture built for AI workloads."
2. **Provisioned Machine resource type**: "Each deployment is provisioned and managed from the cloud using a new type of resource called Provisioned Machine that looks and behaves a lot like an Azure VM."
3. **Foundry Local on Linux infrastructure (preview)**: "Foundry Local is now available as a lightweight container image for Linux infrastructure."
4. **Azure Kubernetes Service on bare metal**: "Azure Kubernetes Service (AKS), the fully-managed enterprise-grade Kubernetes service, now runs directly on bare metal with small form factor deployments – no virtualization layer required."

---

### 5. Azure Cosmos DB — Agent Memory and Agentic Retrieval
**Products**: Azure Cosmos DB, Agent Memory Toolkit, Agentic Retrieval Toolkit, Microsoft Foundry
**Blog**: https://aka.ms/build26/CosmosDBAgents

1. **Agent Memory Toolkit (public preview)**: "The Agent Memory Toolkit is a Python SDK that helps you add memory to AI agents backed by Azure Cosmos DB."
2. **Agentic Retrieval Toolkit (public preview)**: "The Agentic Retrieval Toolkit is a reference implementation for building multi-step retrieval-augmented generation (RAG) applications on Azure."
3. **Iterative retrieval for complex RAG**: "It retrieves relevant documents, generates a preliminary answer, identifies information gaps, creates follow-up sub-questions, retrieves more evidence, and synthesizes a final grounded answer."
4. **Unified store for documents, vectors, and full-text data**: "Both toolkits build on the same foundation: Azure Cosmos DB for NoSQL as a unified store for documents, vectors, and full-text data, with vector search, full-text search, and hybrid search built in."

---

### 1. Microsoft Marketplace
**Products**: Microsoft Marketplace, Microsoft 365 Copilot, Microsoft Teams, Microsoft Foundry
**Blog**: https://aka.ms/MarketplaceBuildBlog2026

1. **Intelligent discovery (in preview)**: "Microsoft Marketplace is launching intelligent discovery (in preview). Instead of relying on keyword search alone, customers can describe their use case in natural language, and Marketplace surfaces relevant solutions with side-by-side comparisons."
2. **Publish once, get surfaced everywhere**: "Publishing through Marketplace does more than create a listing on the Marketplace storefront. It's a distribution path across Microsoft products customers already use—in their flow of work."
3. **Multiparty private offers expansion**: "This includes the recent expansion of multiparty private offers—now available across 30 countries in Europe, with Australia, Japan, and South Africa coming July 15, 2026."
4. **AI stack sourcing through Marketplace**: "Microsoft Marketplace brings the core components of your AI stack—models, developer tools, and applications—directly into your Azure environment."

### 2. Microsoft Teams Platform
**Products**: Microsoft Teams SDK, Teams developer CLI, Microsoft 365 Agents Toolkit, Developer Portal
**Blog**: http://aka.ms/TeamsPlatform-Build

1. **Teams SDK general availability**: "The Teams SDK accelerates the path from idea to working prototype and is now generally available in Python, JavaScript, and C#."
2. **Targeted messages**: "Agents can now have 1:1 interactions with individuals in a group setting through targeted messages."
3. **Sovereign cloud support**: "Microsoft 365 Agents Toolkit and Developer Portal now support sovereign high-cloud environments, including GCC High and DoD, enabling developers targeting these tenants to run the same agent creation and update flows with built-in cloud-aware handling without the need for manual workarounds."
4. **App support in shared and private channels**: "Your agent is no longer confined to standard channels. With app support now available in shared channels and private channels, you can plug into how real collaboration happens across organizational boundaries and on sensitive projects."

### 3. Work IQ API
**Products**: Work IQ, Microsoft 365 Copilot
**Blog**: https://aka.ms/WorkIQAPI_GA

1. **Work IQ API endpoints generally available June 16**: "Work IQ API endpoints will be generally available June 16, including A2A, a redesigned remote MCP server, and a REST API."
2. **Consumption-based access independent of Copilot licensing**: "Usage is independent of Microsoft 365 Copilot licensing and available on a consumption basis."
3. **10 generic tools via MCP**: "The Work IQ MCP collapses hundreds of operations into just 10 generic tools that provide direct access to Microsoft 365 data (mail, calendar, files, people, chat, and sites) and the ability to act on that data."
4. **getSchema for dynamic discovery**: "getSchema, which allows agents to dynamically discover how data is structured at runtime. Instead of relying on predefined models or integrations, agents can understand what data exists, how it's organized, and how to interact with it as needed."
5. **Rego-based policy engine for security**: "The Work IQ MCP uses a small set of broad permissions to establish high-level access boundaries, while a Rego-based policy engine enforces detailed, context-aware rules on every request."

### 4. Azure Cosmos DB Semantic Reranker
**Products**: Azure Cosmos DB for NoSQL, Semantic Reranker
**Blog**: https://aka.ms/build26/cosmosreranker

1. **Semantic Reranker public preview**: "Today we're thrilled to announce the public preview of Semantic Reranker in Azure Cosmos DB for NoSQL, a new AI-powered capability that improves the relevancy of your search results with just a few lines of code."
2. **AI-powered rescoring and reordering**: "Semantic Reranker takes the results from a query you've already run (e.g., vector search, full-text search, hybrid search, or any other query) and uses an AI model to rescore and reorder them based on relevancy to a user's search phrase or context."
3. **SDK integration across .NET, Python, and Java**: "It's built right into the Azure Cosmos DB SDKs (Python, .NET, and Java), so you can reorder results from any container with minimal code changes."

### 5. Azure Container Apps
**Products**: Azure Container Apps, Azure Container Apps Sandboxes, Azure Container Apps Express
**Blog**: https://aka.ms/aca/build

1. **Azure Container Apps Sandboxes (Public Preview)**: "Azure Container Apps Sandboxes addresses that challenge with a new first-class resource type that provides fast, secure, ephemeral compute environments with built-in suspend and resume capabilities."
2. **Azure Container Apps Express (Public Preview)**: "We recently launched Azure Container Apps Express in public preview - the simplest and fastest way to launch and scale powerful applications on Azure, from zero to hyperscale, without infrastructure decisions."
3. **Confidential Compute generally available**: "Confidential Compute in Azure Container Apps is now generally available, providing hardware-backed Trusted Execution Environments (TEEs) through workload profiles."
4. **Docker Compose for Agents (Public Preview)**: "Docker Compose for Agents on Container Apps (public preview) brings the familiar Compose workflow to agentic applications. Declare models, agents, and MCP tools in a single compose.yaml file and deploy unchanged from laptop to cloud."
5. **Defender for Cloud Serverless Containers Posture**: "Customers can now bring Azure Container Apps environments into Microsoft Defender for Cloud's Serverless Containers Posture experience, helping security teams extend posture management across more of their container estate from a single workflow."
---

## URLs Pending Publication

The following blog posts were not yet publicly accessible at time of index generation and will be added when published.

### Auth-walled (Tech Community sign-in required)
- https://aka.ms/ProjectSolaraBuild2026
- https://aka.ms/build-observability
- https://aka.ms/GroundingAPIBuild2026/
- https://aka.ms/VMSSFlex-OS-Image-Upgrades-Preview
- https://aka.ms/Guest-RDMA-preview-blog
- https://aka.ms/apim/build
- https://aka.ms/build/functions
- https://aka.ms/la/build
- https://aka.ms/AzureBackupCosmosDBpreviewTechBlog
- https://aka.ms/FL_Build_2026

### Not yet resolving
- https://aka.ms/AnyscaleonAzureLaunchBlog