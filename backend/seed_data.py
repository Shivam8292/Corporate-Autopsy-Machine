import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
from langchain_core.documents import Document

load_dotenv()

CORPUS = [
    {
        "company": "Quibi",
        "year": 2020,
        "raised": "$1.75B",
        "content": """
**Primary cause of death:** Mobile-only rigidity matched with terrible timing.

**Failure Factors:**
1. Unnecessary constraint: Quibi limited its content exclusively to mobile devices, fundamentally ignoring consumer preferences for cross-platform viewing. When the pandemic hit, users were stuck at home with massive TVs, rendering the mobile-only pitch useless. 
2. Lack of social vitality: Their app explicitly blocked screenshots and sharing. In a world driven by viral TikToks and Twitter memes, Quibi engineered its own isolation, removing organic growth loops completely.
3. Arrogance in pricing: They assumed consumers would pay $4.99/mo (with ads) or $7.99/mo for an unproven platform before there was any must-watch cultural hit. 

**Financial Autopsy:**
Quibi raised a massive $1.75 billion before a single app download. They projected 7.4 million paid subscribers in year one but stalled at fewer than 500,000—a 93% miss. They burned through $1 billion in 6 months on Hollywood-tier production, spending up to $100,000 per minute on shows that no one watched. Ultimately, they sold their entire content library to Roku for a humiliating $100 million (a 94% value destruction).

**What could have saved it:**
- Launching as a cross-platform OTT app (mobile, web, smart TV).
- Enabling aggressive social sharing, GIF creation, and meme generation natively.
- Buying highly engaged internet-native creators rather than over-paying legacy Hollywood stars who brought no built-in audience to a mobile-first paradigm.

**Lesson for Startups:** Never pre-build an isolated ecosystem based purely on executive assumptions. You cannot force consumer behavior shifts (like locking people to mobile video) without a 10x value proposition, regardless of your war chest.
"""
    },
    {
        "company": "WeWork",
        "year": 2019,
        "raised": "$22B+",
        "content": """
**Primary cause of death:** Catastrophic unit economics masked by tech valuation arbitrage.

**Failure Factors:**
1. Financial smoke and mirrors: WeWork sold itself as a high-margin software-as-a-service (SaaS) company, but in reality, it was a traditional real estate arbitrage firm. They signed 15-to-15 year long-term leases and rented them out on 30-day short-term contracts. This extreme duration mismatch made them existentially fragile to any macro downturn.
2. Governance vacuum: CEO Adam Neumann had total voting control and engaged in profound conflicts of interest, including buying buildings personally and leasing them back to WeWork, and charging the company $5.9 million just for the trademark to the word "We".
3. Reckless diversification: They diverted vital capital to absurd vanity projects: a wave pool company, a coding bootcamp, and "WeGrow"—a primary school. 

**Financial Autopsy:**
WeWork burned through billions of dollars, posting a net loss of $1.9 billion in 2018 against just $1.8 billion in revenue—a negative profit margin. At its peak private valuation, it was marked at $47 billion. During their attempted IPO, public markets peered under the hood and rejected the model violently. Within 6 weeks, the valuation collapsed by 80% to $8 billion, eventually resulting in the company declaring Chapter 11 bankruptcy. Total capital lit on fire exceeded $20 billion.

**What could have saved it:**
- Moving to "asset-light" management agreements where WeWork shares revenue with landlords instead of taking on hard lease liabilities.
- Radical corporate governance overhaul with independent board control over related-party transactions.
- Hyper-focus on the core co-working product and terminating all experimental verticals.

**Lesson for Startups:** Slapping tech branding on a fundamentally low-margin, high-capex traditional business will eventually be exposed by the public markets. Profitability cannot be indefinitely postponed by charisma.
"""
    },
    {
        "company": "Theranos",
        "year": 2018,
        "raised": "$1.4B",
        "content": """
**Primary cause of death:** Unabashed technology fraud and toxic secrecy.

**Failure Factors:**
1. Impossibility of physics: The core premise—running hundreds of complex medical tests on a single drop of capillary blood—was scientifically flawed. Capillary blood from a fingerstick is often contaminated by cellular debris and interstitial fluid, meaning the required dilution made accurate diagnostics literally impossible with their Edison machines.
2. Weaponized NDAs and culture of fear: Employees were heavily siloed and aggressively threatened with litigation if they spoke up about QC failures or the fact that commercial Siemens machines were secretly being used for actual testing instead of the proprietary devices.
3. Lack of peer review: Because the founder claimed "trade secrets," Theranos never published peer-reviewed validation data, an absolute prerequisite in the biomedical industry. The board was packed with politicians and retired generals, possessing zero medical diagnostic expertise.

**Financial Autopsy:**
Raised over $1.4 billion at a peak valuation of $9 billion. Rather than failing gracefully, they generated false blood test results for real patients, endangering lives. The company was ultimately valued at $0, shut down entirely in 2018, and founder Elizabeth Holmes was sentenced to 11.25 years in federal prison for wire fraud. 100% of investor capital was wiped out.

**What could have saved it:**
- Pivoting the mission early from "hundreds of tests on one drop" to "developing localized, micro-fluidic testing for 5 specific assays."
- Hiring a board composed of seasoned pathologists and lab-diagnostic innovators instead of politicians.
- Operating transparently through FDA clearance and peer-reviewed journals before scaling retail partnerships like Walgreens.

**Lesson for Startups:** "Fake it till you make it" only applies to software glitches and MVP mockups, never to highly regulated health and life-or-death hardware. Ignoring physics will eventually result in criminal charges.
"""
    },
    {
        "company": "Juicero",
        "year": 2017,
        "raised": "$120M",
        "content": """
**Primary cause of death:** Ludicrous over-engineering solving a non-existent problem.

**Failure Factors:**
1. Hardware overkill: The Juicero press was an extraordinarily complex machine with a force equivalent to lifting two Tesla cars. Behind the sleek Apple-like exterior were hundreds of custom-machined parts. It was engineered beautifully, but entirely unnecessarily, just to squeeze a soft bag of diced fruit.
2. The manual squeeze test: The fatal wound came when a Bloomberg journalist demonstrated that a human being could simply squeeze the proprietary Juicero bags with their bare hands faster and just as effectively as the $400 ($699 at launch) Wi-Fi-enabled machine. The hardware was instantly rendered functionally obsolete by a pair of human hands.
3. Misaligned subscription model: The company locked users into a DRM-styled ecosystem (the machine scanned QR codes and refused to press expired bags). This created intense friction for consumers who just wanted fresh juice without managing a supply chain in their kitchen.

**Financial Autopsy:**
Raised $120M from elite Silicon Valley VCs including Google Ventures. The machine launched at $699, later deeply discounted to $399 in a desperate pivot. The gross margin on the hardware was profoundly negative; they were losing money on every incredibly complex press sold, hoping to make it back on the $5-7 juice packets. Once the bare-hand squeezing video went viral, sales plummeted 90%. They suspended sales and bought back machines from angry consumers.

**What could have saved it:**
- Completely dropping the hardware and playing purely in the premium packaged cold-pressed juice delivery category.
- Creating a drastically simplified $50 mechanical press instead of a connected IoT device.
- Focusing on B2B deployments (offices, cafes) rather than B2C direct-to-countertop.

**Lesson for Startups:** Do not build a $400 smart solution to a problem that can be solved by hand in ten seconds. Hardware must fundamentally enable a new capability, not just act as a DRM tollbooth for a subscription.
"""
    },
    {
        "company": "Pets.com",
        "year": 2000,
        "raised": "$300M",
        "content": """
**Primary cause of death:** Fundamentally underwater unit economics combined with catastrophic shipping costs.

**Failure Factors:**
1. Fatal shipping math: Pet food and litter are heavy, bulky, and have notoriously low profit margins. The cost to warehouse, pack, and physically ship a 40-pound bag of dog food across the country dwarfed any retail markup. The company was structurally designed to lose more money the faster it grew.
2. Predatory marketing spend over infrastructure: They blew absurd amounts of capital on Super Bowl ads (featuring their famous sock puppet mascot) and Macy's Thanksgiving Day Parade balloons, but entirely failed to establish an efficient logistical supply chain.
3. Extreme discounting: To acquire customers and achieve "eyeballs" and scale (the mantra of the Dot-com bubble), they frequently sold items below cost and subsidized shipping. Their customer acquisition cost (CAC) drastically exceeded the lifetime value (LTV) of their customers.

**Financial Autopsy:**
Completed a highly publicized IPO in early 2000 raising $82.5 million, peaking at $14 per share. In its first fiscal year, it spent $11.8M on advertising to generate just $619,000 in revenue. When the dot-com bubble popped, institutional investors refused to infuse more cash into a business with negative 30% gross margins. 268 days after their IPO, the stock traded at $0.19 and the company liquidated.

**What could have saved it:**
- Localized distribution hubs restricting sales of heavy/low-margin items only to dense urban zones where last-mile delivery made sense.
- Focusing purely on high-margin, lightweight items (medications, premium pet toys, niche accessories).
- Axing national television ad campaigns until backend fulfillment economics achieved positive gross margins.

**Lesson for Startups:** E-commerce is not purely a software game; it is constrained by physics and logistics. If you lose money on every transaction, making it up in volume is a mathematical impossibility. CAC < LTV is gravity.
"""
    },
    {
        "company": "Friendster",
        "year": 2011,
        "raised": "$50M",
        "content": """
**Primary cause of death:** Technical scaling paralysis resulting in fatal user experience decay.

**Failure Factors:**
1. Database architecture collapse: Friendster grew so rapidly that their infrastructure buckled. They wrote complex features on top of an unoptimized backend, leading to page load times exceeding 40 seconds. Users were staring at error screens more than profiles. Instead of pausing features to fix infra, they ignored it.
2. Arrogant response to users: When users created "Fakesters" (profiles for dogs, cities, or concepts), the company aggressively deleted them, stifling the exact emergent, playful behavior that makes a social network sticky. They failed to listen to how their users organically wanted to use the product.
3. Hubris in acquisitions: In 2003, they famously rejected a $30M acquisition offer from Google (which would be worth billions in Google stock today), believing they were unstoppable. As load times worsened, users defected en masse to a faster, cleaner upstart called MySpace.

**Financial Autopsy:**
Raised over $50 million, hitting an initial peak valuation of over $100M. Despite the heavy capitalization, they lost their entire US user base within 36 months to MySpace. They managed a secondary resurgence in Southeast Asia before Facebook annihilated that market as well. Eventually sold for roughly $40M to a Malaysian payments company—a distressed asset sale representing a fraction of their peak potential.

**What could have saved it:**
- Halting all new feature development to execute a total backend rewrite ensuring sub-second page loads.
- Embracing rather than banning emergent user behaviors (leaning into meme accounts and brand pages instead of deleting them).
- Taking the Google payout, recognizing that consumer social is hyper-volatile.

**Lesson for Startups:** Technical debt in a consumer social product is fatal. If the core loop (page load) breaks, switching costs are essentially zero. Users will abandon you overnight for a faster clone.
"""
    },
    {
        "company": "Fab.com",
        "year": 2015,
        "raised": "$330M",
        "content": """
**Primary cause of death:** Hysterical over-expansion fueled by venture capital gluttony.

**Failure Factors:**
1. Premature scaling/expansion: Upon seeing early success in flash-sales for indie design goods in the US, Fab aggressively launched in Europe. They bought European clone startups, hired hundreds of people in Berlin, and established massive warehouses before proving the model could sustain overseas. The overhead killed them.
2. Inventory pivot chaos: They shifted from a zero-inventory flash-sales model (holding no stock, shipping from designers) to a traditional retail model holding massive amounts of inventory. This decimated their working capital and transformed a lean tech platform into a heavy, slow retailer.
3. Loss of core identity: Initially, Fab.com was curated, quirky, and premium. To hit massive VC-mandated growth targets, they started selling everything from cheap plastic toys to pet food. They alienated their core loyal user base to chase general Amazon-like commerce, failing at both.

**Financial Autopsy:**
Raised an astonishing $330M, reaching a peak valuation of $1 billion ("unicorn" status). As the European expansion bled cash, their monthly burn rate hit $14M. Sales flatlined while user acquisition costs soared. They executed four distinct rounds of massive layoffs, cutting from 700 employees down to 15. Finally, the $1 billion company was essentially sold for parts to PCH International for a pitiful $15 million. 

**What could have saved it:**
- Remaining hyper-disciplined and geographically constrained: winning the US completely before spending a dime across the Atlantic.
- Refusing to pivot away from the flash-sale dropship model, keeping working capital lightweight.
- Accepting a smaller, sustainable $100M valuation business rather than torching the brand to chase a $10B IPO pipe dream.

**Lesson for Startups:** Lethal amounts of funding can cause startups to die of indigestion rather than starvation. Premature scaling destroys both company culture and unit economics.
"""
    },
    {
        "company": "Jawbone",
        "year": 2017,
        "raised": "$900M+",
        "content": """
**Primary cause of death:** Manufacturing dysfunctions and being crushed in a highly commoditized hardware market.

**Failure Factors:**
1. Crippling quality control: Their flagship fitness tracker, the UP band, suffered from catastrophic failure rates. Many devices hard-bricked within weeks of purchase due to water ingress and battery failure. Jawbone had to issue mass refunds and replace bands, destroying margins and brand trust instantly.
2. The squeeze play: They were caught directly in the death zone of the hardware barbell. On the low end, Xiaomi and Fitbit produced cheaper, more reliable step counters. On the high end, the Apple Watch launched, utterly destroying the premium standalone fitness band market by integrating tracking into a full smart ecosystem.
3. Endless pivoting: With hardware failing, they tried to pivot into a "health data" machine learning company relying on "clinical grade" tracking, but the runway was too short and their reputation with consumers was already shattered.

**Financial Autopsy:**
Jawbone raised over $900M from marquee investors (Sequoia, a16z, Khosla). At its peak, it was valued at $3.2 billion. Once the Apple Watch hit, Jawbone's market share evaporated. Their final valuation was effectively zero when they were forced into liquidation. It stands as one of the most spectacularly expensive VC failures in Silicon Valley history, returning exactly nothing to common shareholders.

**What could have saved it:**
- Executing a software/data pivot much earlier, positioning Jawbone as the hardware-agnostic health intelligence app layer rather than competing on bracelets.
- Radically simplifying the hardware to ensure 99.9% reliability before national rollouts.
- Selling to a legacy health conglomerate in 2014 before Apple systematically consumed the category.

**Lesson for Startups:** Consumer hardware without a deep, defensible moat is a race to zero margins. You cannot out-compete Apple on premium ecosystem design, nor out-compete Chinese manufacturing on price. You must own the data layer.
"""
    }
]

def ingest_baseline_data():
    try:
        print("Starting ChromaDB local ingestion for failure corpus...")
        vectorstore = Chroma(
            collection_name=os.getenv("COLLECTION_NAME", "startup_failures"),
            persist_directory=os.getenv("CHROMA_PATH", "./chroma_db"),
            embedding_function=HuggingFaceEmbeddings(
                model_name=os.getenv("EMBED_MODEL", "all-MiniLM-L6-v2")
            )
        )
        
        # Prevent duplicate insertion if already exists
        count = vectorstore._collection.count()
        if count > 0:
            print(f"Collection already has {count} documents. Skipping seed.")
            return

        splitter = RecursiveCharacterTextSplitter(chunk_size=800, overlap=150)
        docs = []

        for item in CORPUS:
            chunks = splitter.split_text(item["content"])
            for idx, chunk in enumerate(chunks):
                doc = Document(
                    page_content=chunk,
                    metadata={
                        "company": item["company"],
                        "year": item["year"],
                        "raised": item["raised"],
                        "source": f"{item['company']}_postmortem"
                    }
                )
                docs.append(doc)
        
        vectorstore.add_documents(docs)
        print(f"Ingestion complete. Added {len(docs)} chunks to ChromaDB.")
    except Exception as e:
        print(f"Error during ingestion: {e}")

if __name__ == "__main__":
    ingest_baseline_data()
