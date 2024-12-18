# # ai_model.py or models.py
# from langchain.llms import HuggingFacePipeline
# import transformers
# import torch

# def get_model_response(prompt):
#     model = "daryl149/llama-2-7b-chat-hf"
#     tokenizer = transformers.AutoTokenizer.from_pretrained(model)
#     pipeline = transformers.pipeline(
#         "text-generation",
#         model=model,
#         tokenizer=tokenizer,
#         torch_dtype=torch.bfloat16,
#         trust_remote_code=True,
#         device_map="auto",
#         max_length=1000,
#         do_sample=True,
#         top_k=10,
#         num_return_sequences=1,
#         eos_token_id=tokenizer.eos_token_id
#     )
#     llm = HuggingFacePipeline(pipeline=pipeline, model_kwargs={'temperature': 0})
#     return llm(prompt)
