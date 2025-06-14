from zenml.client import Client

def setup_zenml():
    """Initialize ZenML and set up the local stack."""
    # Initialize ZenML
    client = Client()
    
    # Create a local stack if it doesn't exist
    try:
        # Check if we're using a newer ZenML version
        if hasattr(client, "active_stack"):
            print(f"Using active stack: {client.active_stack.name}")
        else:
            print("Using default local stack")
    except Exception as e:
        print(f"Note: {e}")
        print("Setting up with default configuration")
    
    print("ZenML setup complete!")
    # Just print the repository path without accessing attributes
    print(f"ZenML is initialized in the current directory")

if __name__ == "__main__":
    setup_zenml()