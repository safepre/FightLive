import sys
import asyncio
from src.main import main

from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))


from src.main import main

if __name__ == "__main__":
    asyncio.run(main())
