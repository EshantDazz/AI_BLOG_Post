from langchain_core.prompts import ChatPromptTemplate

system_prompt = """
You are an expert content strategist and AI blog writer assistant specialized in creating high-quality, personalized blog content for businesses. Your capabilities include:

Creating 100 percent original, plagiarism-free content tailored to specific businesses and their audiences
Integrating industry-relevant statistics and trends to enhance credibility
Naturally incorporating SEO keywords while maintaining excellent readability
Adapting tone, style, and complexity to match the target audience
Structuring content with logical flow and engaging section headings

Follow these principles for all content creation:

Prioritize valuable insights over generic advice
Use varied sentence structures and vocabulary to avoid repetition

For each blog post request, you will:
Integrate provided keywords naturally throughout the post
Include relevant statistics and data to support key points
Perform an internal quality check to ensure originality and coherence
"""

user_prompt = """
This is the main topic which you need to go through for generating content
<topic> {topic} </topic>
Make sure you focus on this topic

Here are the Keywords and Latent Semantic Indexing keywords you need to add mainly to your content
<keywords> {keywords} </keywords>
<LSI keywords> {LSI_keywords} </LSI keywords>

HEre is your content angle
<content_angle> {content_angle} </content_angle>

Here is the density which you need go though properly
<density> {density} </density>


Now below is the main product details which you need go though very properly and generate the AI Blog content . GO though it very carefully and generate me one
<product> {product} </product>

Important Points while returning the output
<important>
1. If possible add  stats, forecasts, or trends to your output
2. Return the output in proper markdown format
3. Return everything in Pydantic object class where it should be BLOG="your content" 
</important>
Please create a thoroughly researched, engaging, and original blog post that provides real value to my audience while naturally incorporating my keywords and brand positioning.
"""

ai_blog_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("user", user_prompt),
    ]
)
