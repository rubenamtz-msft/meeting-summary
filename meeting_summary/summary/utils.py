from .models import Meeting
from .inference import summarize
import uuid
from timeit import default_timer

MAX_NUMBER_WORDS = 499


def super_algorithm(meeting_id):
    # captions = Caption.objects.filter(meeting__id=meeting_id).order_by("index")
    meeting = Meeting.objects.filter(id=meeting_id).first()
    captions = meeting.captions

    last_index = 0
    caption_list = []
    while True:
        
        captions = captions[last_index:]
        if not captions:
            return caption_list
        caption_subset, last_index = get_caption_subset(captions)
        

        caption_list.append(caption_subset)

def get_caption_subset(captions, max_num_words=MAX_NUMBER_WORDS):
    num_words = 0
    caption_subset = []
    last_name = captions[0].get("name",None)
    last_index = 0

    for caption in captions:
        current_name = caption.get("name", None)
        num_words += len(caption.get("text", None).split(" "))
        if num_words < max_num_words and current_name == last_name:
            caption_subset.append(caption)
            last_index = captions.index(caption) + 1
        else:
            if last_index == 0:
                last_index = 1
                caption_subset.append(caption)
            return caption_subset, last_index
    return caption_subset, last_index
    
def join_caption_texts(caption_subset):
    result = dict()
    result["start"] = caption_subset[0].get("start",None)
    result["end"]   = caption_subset[-1].get("end",None)
    result["name"]  = caption_subset[0].get("name",None)
    if len(caption_subset) > 1:
        result["text"] = " ".join([caption.get("text",None) for caption in caption_subset])
    else:
        result["text"] = caption_subset[0].get("text", None)
    return result

def inference(result):
    text = result.get("text", None)
    start = result.get("start", None)
    #print(f"{result['name']}: {text}")
    if len(text.split(" ")) < 50:
        return text, start
    else:
        # run inference
        y = summarize(text)
        return y, start

def produce_summary(caption_list):
    response = list()
    start_outer = default_timer()
    for caption_subset in caption_list:
        result = join_caption_texts(caption_subset)
        start_inner = default_timer()
        y, start = inference(result)
        duration = default_timer() - start_inner
        print("Duration Inner Inference ",duration)

        #print(f"Summary: {y}, with timestamp {start}")
        # use a serializer to produce a response or not
        response.append({
            "id": str(uuid.uuid4()),
            "summary": y,
            "properties": {
                "source": {
                    "id": str(uuid.uuid4()),
                    "text": result["text"],
                    "start": result["start"]
                },
                "words_count": len(y.split(" ")),
                "name": result["name"]
            }
        })
    duration = default_timer() - start_outer
    print("Duration INFERENCE OF ALL CAPTIONS ",duration)
    
    return response
