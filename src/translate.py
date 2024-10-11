from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
import logging

def translate_text(text, config):
    logging.info("Translating text...")
    model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M")
    tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")
    
    tokenizer.src_lang = "auto"
    encoded = tokenizer(text, return_tensors="pt")
    
    generated_tokens = model.generate(**encoded, forced_bos_token_id=tokenizer.get_lang_id(config['translation']['target_language']))
    return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]