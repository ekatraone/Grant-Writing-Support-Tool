# # ai_model.py (in grant_writer_app)
# # from langchain.llms import HuggingFacePipeline
# from langchain_community.llms import HuggingFacePipeline  
# import transformers
# import torch
# import os

# # Ensure the offload folder exists
# os.makedirs("offload_weights", exist_ok=True)

# def get_model_response(prompt):
#     model = "daryl149/llama-2-7b-chat-hf"
#     tokenizer = transformers.AutoTokenizer.from_pretrained(model, legacy=False)
#     pipeline = transformers.pipeline(
#         "text-generation",
#         model=model,
#         tokenizer=tokenizer,
#         torch_dtype=torch.bfloat16,
#         # trust_remote_code=True,
#         device_map="auto",
#         offload_folder="./offload",  # Specify offload folder for disk storage
#         max_length=1000,
#         do_sample=True,
#         top_k=10,
#         num_return_sequences=1,
#         eos_token_id=tokenizer.eos_token_id
#     )
#     llm = HuggingFacePipeline(pipeline=pipeline, model_kwargs={'temperature': 0})
#     return llm(prompt)
