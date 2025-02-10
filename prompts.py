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
0 indicates no relevance at all, 1 indicates very little relevance, 2 indicates 
minor topic of the article, 3 indicates a sub topic of the article, and 4 indicates a major 
topic of the article. It may happen that an article is entirely unrelated to the different categories.
In this case, all weights should be set to 0. If an article fits two or more categories, 
there should be only one major category with a value of 4.
All other categories should have lower values.

## Examples

```
{BR_O}
    "reason": "{EXAMPLE_RATE_0}",
    "smart citities and mobility": 0,
    "trade logistics and ecommerce": 0,
    "manufacturing": 0,
    "green tech climate and energy": 1,
    "health tech": 0,
    "mine tech": 0,
    "creatives": 0,
    "fin tech": 4,
    "argi tech": 2,
    "tourism": 0,
    "ed tech": 0
{BR_C}
```

```
{BR_O}
    "reason": "{EXAMPLE_RATE_1}",
    "smart citities and mobility": 0,
    "trade logistics and ecommerce": 0,
    "manufacturing": 0,
    "green tech climate and energy": 0,
    "health tech": 4,
    "mine tech": 0,
    "creatives": 0,
    "fin tech": 0,
    "argi tech": 0,
    "tourism": 0,
    "ed tech": 3
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
    "smart citities and mobility": (
        "Smart cities are integrating advanced technologies such as artificial intelligence, IoT, and data "
        "analytics to create efficient, sustainable, and connected mobility systems that optimize "
        "transportation infrastructure and reduce congestion."),
    "trade logistics and ecommerce": (
        "The rise of digital platforms and e-commerce has transformed the trade, logistics, and supply chain "
        "landscape by providing real-time tracking, streamlined payment options, and increased efficiency in "
        "shipping and delivery processes."),
    "manufacturing": (
        "Advances in Industry 4.0 technologies such as robotics, artificial intelligence, and the Internet of "
        "Things (IoT) are transforming traditional manufacturing by enabling greater efficiency, flexibility, "
        "and precision in production processes."),
    "green tech climate and energy": (
        "The rapid growth of renewable energy sources such as solar and wind power, combined with electric "
        "vehicles and energy-efficient technologies, is driving a global shift towards a low-carbon economy "
        "and sustainable energy future."),
    "health tech": (
        "Artificial intelligence (AI) and machine learning (ML) technologies are being increasingly used in "
        "healthcare to analyze large amounts of medical data, identify patterns, and develop predictive "
        "models to improve patient care and outcomes."),
    "mine tech": (
        "Mining technology is leveraging innovations such as autonomous haulage systems, drones, and machine "
        "learning algorithms to increase efficiency, reduce costs, and improve safety in the extraction of "
        "minerals and metals."),
    "creatives": (
        "The intersection of technology and creativity is driving innovation in the creative industries, with "
        "advancements in areas such as virtual reality, augmented reality, and artificial intelligence "
        "enabling new forms of storytelling, collaboration, and artistic expression."),
    "fin tech": (
        "Financial technology (FinTech) is transforming the way people manage their finances, invest, borrow, "
        "and save by leveraging digital platforms, mobile apps, and blockchain technologies to increase "
        "accessibility, efficiency, and security."),
    "argi tech": (
        "Agricultural technology (AgTech) is using precision farming methods, drones, satellite imaging, and "
        "big data analytics to optimize crop yields, reduce waste, and improve resource allocation in the "
        "agricultural sector, enhancing food production and sustainability."),
    "tourism": (
        "The rise of digital technologies such as social media, online booking platforms, and mobile apps is " 
        "revolutionizing the tourism industry by providing travelers with more personalized, efficient, and "
        "immersive experiences, as well as enabling destinations to promote themselves more effectively."),
    "ed tech": (
        "Education technology (EdTech) is leveraging digital platforms, learning management systems, and "
        "innovative tools such as AI-powered adaptive learning and virtual reality to improve access, "
        "engagement, and outcomes in education, enabling personalized learning experiences for students of "
        "all ages.")
}

RATING_INNOVATIONS_IN_AFRICA = replacer(
    RATING_PROMPT,
    {
        "topic": "innovations in Africa",
        "categories": ", ".join(
            [f"'{cat}'" for cat in sorted(CATEGORIES.keys())]),
    })