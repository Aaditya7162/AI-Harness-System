import sys
from agent import AutonomousAgent

def main():
    print("Welcome to the Autonomous AI Harness!")
    
    # Initialize the agent
    agent = AutonomousAgent()
    
    if len(sys.argv) > 1:
        # Task passed via command line arguments
        task = " ".join(sys.argv[1:])
        print(f"Executing task: {task}")
        agent.run(task)
    else:
        # Interactive loop
        while True:
            try:
                task = input("\nEnter your task (or 'exit' to quit): ")
                if task.lower() in ['exit', 'quit']:
                    break
                if not task.strip():
                    continue
                
                print("--- Agent is thinking ---")
                agent.run(task)
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
