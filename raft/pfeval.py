import os
import json
#from datetime import datetime
from promptflow.core import AzureOpenAIModelConfiguration
from promptflow.evals.evaluators import RelevanceEvaluator, GroundednessEvaluator, FluencyEvaluator, CoherenceEvaluator, SimilarityEvaluator
#from promptflow.evals.evaluate import evaluate
from dotenv import load_dotenv
import argparse
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from logconf import log_setup

logger = logging.getLogger("pfeval")

load_dotenv()

def get_args() -> argparse.Namespace:
    """
    Parses and returns the arguments specified by the user's command
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=str, default="input.jsonl", help="The input data JSONL file to load")
    parser.add_argument("--output", type=str, default="output.jsonl", help="The output data JSONL file to export to")

    args = parser.parse_args()
    return args

#def evaluate_aistudio(model_config, data_path):
#    # create unique id for each run with date and time
#    run_prefix = datetime.now().strftime("%Y%m%d%H%M%S")
#    run_id = f"{run_prefix}_chat_evaluation_sdk"    
#    print(run_id)
#
#    result = evaluate(
#        evaluation_name=run_id,
#        data=data_path,
#        evaluators={
#            #"violence": violence_eval,
#            "relevance": RelevanceEvaluator(model_config),
#            "fluency": FluencyEvaluator(model_config),
#            "coherence": CoherenceEvaluator(model_config),
#            "groundedness": GroundednessEvaluator(model_config),
#        },
#        evaluator_config={
#            "defaults": {
#                "question": "${data.question}",
#                "answer": "${data.gold_answer}",
#                "context": "${data.context}",
#            },
#        },
#    )
#    return result

def evaluate_local(model_config, data_path):
    data = []
    with open(data_path) as f:
        for line in f:
            data.append(json.loads(line))

    evaluators = [
        RelevanceEvaluator(model_config),
        FluencyEvaluator(model_config),
        CoherenceEvaluator(model_config),
        GroundednessEvaluator(model_config),
        SimilarityEvaluator(model_config),
    ]

    def evaluate_row(row):
        output = {
            'query': row['question'], 
            'response': row['gold_answer'], 
            'context': row['context']
        }
        for evaluator in evaluators:
            result = evaluator(
                question=row['question'],
                answer=row['gold_answer'],
                context=row['context']
            )
            output.update(result)
        return output

    results = []
    futures = []
    with tqdm(total=len(data)) as pbar:
        with ThreadPoolExecutor() as executor:
            for row in data:
                futures.append(executor.submit(evaluate_row, row))
            for future in as_completed(futures):
                results.append(future.result())
                pbar.update(1)

    return results

if __name__ == "__main__":
    import time
    import jsonlines

    log_setup()
    args = get_args()

    # Initialize Azure OpenAI Connection
    logger.info("Loading model configuration")

    deployment = os.environ["AZURE_OPENAI_DEPLOYMENT"]
    api_key=os.environ["AZURE_OPENAI_API_KEY"]
    api_version=os.environ["OPENAI_API_VERSION"]
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]

    logger.info(f"deployment=f{deployment}")
    logger.info(f"api_version=f{api_version}")
    logger.info(f"azure_endpoint=f{azure_endpoint}")

    model_config = AzureOpenAIModelConfiguration(
            azure_deployment=deployment,
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=azure_endpoint
        )

    start=time.time()
    logger.info(f"Starting evaluate...")

    eval_result = evaluate_local(model_config, data_path=args.input)

    end=time.time()
    logger.info(f"Finished evaluate in {end - start}s")
    logger.info(f"Writing {len(eval_result)} results to {args.output}")

    #save evaluation results to a JSONL file
    with jsonlines.open(args.output, 'w') as writer:
        writer.write_all(eval_result)
