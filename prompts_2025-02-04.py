def replacer(text: str, mapping: dict[str, str]) -> str:
    """
    Replaces the keys of the dictionary in the provided text with their values.

    Args:
        text (str): The text.
        mapping (dict[str, str]): The replacement mapping. Keys will be
            surrounded by `<key>` for replacement.

    Returns:
        str: The substituted string.
    """
    for key, value in mapping.items():
        text = text.replace(f"<{key}>", value)
    return text.strip()

BR_O = "{"
BR_C = "}"

EXAMPLE_RATE_0 = (
    "The article presents an online investment platform that connects investors with sustainable agricultural projects. "
    "It features diverse projects, uses blockchain for transparency, and IoT for real-time data. "
    "The solutions is aimed at individual investors interested in sustainable development and agriculture."
)

EXAMPLE_RATE_1 = (
    "The article presents an online platform that healthcare professionals "
    "can use to receive training, publish their work experiences in fighting against malaria, "
    "and interact with other professionals."
)

RATING_PROMPT = f"""
You are a knowledgeable assistant that rates articles about <topic> on how
much they focus on the given categories. Most articles are in English.
However, some articles are in French, and others in Spanish.
The categories are:

<categories>

There are no other categories. Your entire response is a JSON and nothing else. 
The JSON is an object with several fields: "reason" which provides a short 
(50 - 100 words) justification in English for your assessment and one numeric field for 
every category. The numbers indicate the weight of each category in the article. 
0 indicates the category is not relevant at all, 1 indicates it is marginally relevant, 
2 indicates it is somewhat relevant, 3 indicates the category is relevant to the article, 
and 4 indicates that the category is a topic of the article. It may happen that an article 
is entirely unrelated to the different categories. In this case, all weights should be set to 0. 
If an article fits two or more categories,  there should be only one major category 
with a value of 4. All other categories should have lower values.

## Examples

```
{BR_O}
    "reason": "{EXAMPLE_RATE_0}",
    "cities/mobility": 0,
    "ecommerce/logistics": 0,
    "manufacturing": 0,
    "green/climate/energy": 1,
    "healthtech": 0,
    "minetech": 0,
    "creative": 0,
    "fintech": 4,
    "agritech": 2,
    "tourism": 0,
    "edtech": 0
{BR_C}
```

```
{BR_O}
    "reason": "{EXAMPLE_RATE_1}",
    "cities/mobility": 0,
    "ecommerce/logistics": 0,
    "manufacturing": 0,
    "green/climate/energy": 0,
    "healthtech": 4,
    "minetech": 0,
    "creative": 0,
    "fintech": 0,
    "agritech": 0,
    "tourism": 0,
    "edtech": 3
{BR_C}
```
"""

# There are no other categories. Your entire response is a JSON and nothing else. 
# The JSON is an object with several fields: "reason" which provides a short 
# (50 - 100 words) justification in English for your assessment and one numeric field for 
# every category. The numbers indicate the weight of each category in the article. 
# 0 indicates no mention at all, 1 indicates a brief acknowledgement, 2 indicates 
# a minor mention, 3 indicates a sub topic of the article, and 4 indicates a major 
# topic of the article.

CATEGORIES = {
    "cities/mobility": (
        "Rapid urbanization across Africa necessitates innovative solutions in smart cities and mobility. This sector "
        "focuses on improving urban infrastructure, transportation, and creating sustainable urban environments, "
        "addressing the challenges and opportunities presented by Africa's urban growth."),
    "ecommerce/logistics": (
        "The E-Commerce, Logistics, and TradeTech sector is fundamental in enhancing intra-African trade, a critical "
        "component for regional economic integration. Startups in this sector are instrumental in reducing costs, "
        "increasing transparency, and optimizing trade processes, contributing to a more connected and efficient "
        "African market."),
    "manufacturing": (
        "Manufacturing technologies are tech enabled tools and processes that improve the efficiency, quality, and"
        " productivity of the manufacturing sector. These technologies can range from smart factories, industrial"
        " internet of things, data analytics, product design and predictive maintenance, robotics and automation, AI"
        " and machine learning, machine health monitoring, maintenance management systems. Manufacturing technologies"
        " are also the basis for the fourth industrial revolution."),
    "green/climate/energy": (
        "In the face of climate change, the Green/Climate/Energy sector represents an essential area of focus. "
        "Innovations in solar energy, wind technology, waste-to-energy, and water desalination projects are imperative "
        "for mitigating environmental impacts. This sector's growth is evidenced by its significant share of "
        "investment, highlighting the continent's move towards sustainable solutions. Desirable solutions include "
        "innovations that expand access to reliable and affordable energy, for example through the following pathways."
        " Digitalisation: Leveraging digital technologies, Distributed Ledger Technology (DLT), and the Internet of"
        " Things (IoT) to optimize energy production, distribution, and consumption; Energy Efficiency Technology:"             "Technologies that improve energy usage efficiency in various sectors. "
        "Low Carbon & Capture Technology: Innovations that reduce carbon emissions and enhance carbon capture. "
        "Innovative Business Models: New business approaches that drive the adoption of clean energy solutions. "
        "Smart Grid: Solutions that enhance grid management, stability, and integration of renewable energy sources. "
        "Energy Storage: Technologies that improve the storage and distribution of energy, particularly from "
        "intermittent renewable sources. Clean/Renewable Energy: Advancements in the generation of clean and renewable "
        " energy. Sustainable Mobility: Innovations in transportation that reduce carbon emissions and promote "
        "sustainability. Energy Management: Tools and systems that enhance the management of energy resources, "
        "improving efficiency and sustainability. "),
    "healthtech": (
        "Artificial intelligence (AI) and machine learning (ML) technologies are being increasingly used in "
        "healthcare to analyze large amounts of medical data, identify patterns, and develop predictive "
        "models to improve patient care and outcomes. Startups with an emphasis in the following areas are strongly"
        " encouraged: (1)Disease Prevention: - Early detection technologies - Predictive health analytics - Lifestyle"
        " intervention. (2) Clinical Preventive Frameworks and Community Advocacy: - Public health outreach solutions. "
        "(3) Community health worker support systems - Health education and awareness platforms. (4) Vaccine and "
        "Medicine Production: - Novel vaccine development technologies - Local pharmaceutical manufacturing solutions "
        "- Drug discovery platforms. (5) Medical Robotics and Automation (MRA): - Surgical robotics - Automated "
        "diagnostic systems - AI-assisted medical procedures. (6) Genomics: - Personalized medicine solutions -"
        "Genetic testing and counselling platforms - Gene therapy technologies. (7) Biomedical Systems: - Advanced "
        "medical imaging - Biomedical sensor technologies - Tissue engineering and regenerative medicine. "
        "(8) Patient Care Journey: - Telemedicine and remote patient monitoring - Electronic health records and data"
        " management –Patient engagement and adherence solutions. (9) Pandemic/health emergencies management. "
        "Malnutrition and stunting. (10) Monetisation Strategies."),
    "minetech": (
        "Mining technology is leveraging innovations such as autonomous haulage systems, drones, and machine "
        "learning algorithms to increase efficiency, reduce costs, and improve safety in the extraction of "
        "minerals and metals. Focus areas include: Waste management and efficient mineral recovery. Data visualization"
        " and interpretation. Drone applications and surveying. Sustainability-focused mining innovations."),
    "creative": (
        "The creative sector offers a wealth of opportunities for Africa's youth, spanning digital entertainment and "
        "marketing. This sector plays a crucial role in reshaping the global perception of Africa, promoting cultural "
        "exports, and fostering economic integration into the global market."),
    "fintech": (
        "The FinTech sector in Africa has demonstrated remarkable growth, showcasing a vast potential to revolutionize "
        "financial inclusion. By dismantling traditional barriers to financial services, FinTech startups are pivotal "
        "in enhancing access to banking, credit, and investment opportunities, thereby contributing to the achievement "
        "of various Sustainable Development Goals (SDGs). This sector's dynamic growth attracts both local and "
        "international investors, enriching the ecosystem with diverse funding opportunities."),
    "agritech": (
        "AgriTech addresses the vital challenge of food security in a continent where agriculture is a cornerstone of"
        " the economy. Through advancements in robotics, artificial intelligence, IoT, and traceability technologies,"
        " AgriTech innovations are set to enhance agricultural productivity and streamline supply chains, ensuring food"
        " availability and sustainability."),
    "tourism": (
        "TourismTech has significant potential to attract tourists, promote sustainable tourism. It leverages"
        " technology to manage tourism's environmental and societal impacts, contributing to Africa's social and"
        " economic development."),
    "edtech": (
        "EdTech has significant potential to address the educational needs of the continent. It leverages technology to"
        " enhance educational access, and provide innovative learning solutions, contributing to Africa's social and"
        " economic development.")
}

RATING_INNOVATIONS_IN_AFRICA = replacer(
    RATING_PROMPT,
    {
        "topic": "innovations in Africa",
        "categories": ", ".join(
            [f"'{cat}'" for cat in sorted(CATEGORIES.keys())]),
    })