Name: Kenneth Frederick Rebello
PRN: 1132232029
Email: kennethrebello253@gmail.com
Contact: 8317390275 / 8495030275
College: MIT World Peace University Pune Maharashtra 411004.

Youtube Video for Working Link:
Will be uploaded in my project readme.

Hi there, welcome to this documentation of Grant Writing Support Tool. I’m Kenneth Rebello and I have built this tool with a large language model of Meta Llama. This tool will enhance your grant writing process. So Welcome to my exciting Journey of building this project.

What is Grant Writing?
Grant writing is the process of preparing and submitting a proposal to request funding from a government agency, foundation, corporation, or other funding organization. This process is typically undertaken by individuals, nonprofit organizations, or businesses seeking financial support for specific projects, programs, or initiatives.
Lets see the problem statement:
In the traditional method of grant writing, people would write grants with the help of books and would conduct a lot of research. With the help of GrantAI – A LLM and generative AI based Grant writing support tool that helps you to generate grants with  

Before Enhancement	After Enhancement
Limited to static grant-writing resources and templates.	Dynamic, AI-driven personalized suggestions for grant proposal improvement.
Users manually search for relevant resources and guidance.	Users receive real-time, context-aware recommendations based on their input.
Users spend more time researching and editing proposals.	Faster proposal creation process with immediate suggestions from AI.





My Updates:
Tech Stack: Python, Django, meta-llama/Llama-2-7b-chat-hf, Tailwind CSS, Langchain.

I have created a User interface Page where the user will enter his prompts to the model and the requests would be processed by the model and results will be generated.

 

Implementation:
Task 1: Research.
Research plays an important role to innovate and build something. So I thoroughly researched about what is grant writing and about the existing system.
Task 2: Forking the repository.
I forked the repository using Github and then cloned it to my local system and then initialized my first commit and pushed it to the remote repository but to the branch repository and not the main.


Task 3: Planning and Defining the flow of project:
This phase included several steps to plan and create a flow. Some ideas included
•	Search for an ebook on google and use the pdf version as data. The steps later include converting the data into chunks, overlapping it and then embedding it to a vector database like pinecone using a embedding model.
•	Later embedding a LLM to it so that it can creatively generate responses.
•	This also included defining the tech stack and the requirements of the project such as what python libraries will be required for the implementation.
•	Then creating a final flow for the project and following it.

Task 4: Implementation Experiment:
This phase includes experimenting on models and finalizing. (used notebook ipynb file)
•	Whenever we work with GenAI projects firstly we have to experiment on it.
•	I used a Neo-GPT model at the beginning for my project, but later the problem was that it did not give accurate results and was not that useful.
•	Since I had Meta Llama license I decided to use a larger model so that I could get accurate results.

Task 5: Integrating the project to Django:
This phase included creation of an interface with the help of Django
•	Wrote the logic for the working of the model that included handling requests and generating responses.
•	Created and designed HTML files (templates) with tailwind CSS to give it a clean user interface.
Task 6: Creating a Pull Request:
The final Step
•	Once all the files were committed and updated, I created a pull request to the repository from where I had forked the project.
Experiment.ipynb File: (Google Collab)
https://colab.research.google.com/drive/1tNdwAtct8a5qsQutTOyu3tD4oGR-UCUM?usp=sharing

AIML Tools Used:
Model: meta-llama/Llama-2-7b-chat-hf (Large language Model used to generate texts according to the prompts)
Frameworks: 
•	HuggingFace Transformers: For text generation.
•	PyTorch
•	Django
•	Langchain
•	HuggingFacePipeline (Connecting to model)

Challenges:
•	Integrating the model with Django.
•	Large response time due to a large model and lack of  GPU Resources.
Screenshots:
 

 

Prompts:
prompt="Write a grant proposal for a funding of Rupees 50,000 for a project to take care of Street animals."

Response:
 


Links:
Github: https://github.com/Kenneth3120
LinkedIn:  http://www.linkedin.com/in/kenneth-rebello
Blogger: https://kennethfrebello.blogspot.com/2024/12/how-does-chatgpt-describe-you.html


