# Folder Structure Metadata Extraction

## Overview

The Election Monitoring System now includes the ability to extract metadata from folder structures when processing files. This feature enhances the system's ability to organize and categorize election data based on the hierarchical structure of the data folders.

## Folder Structure

The system expects a specific folder structure for optimal metadata extraction:

```
data/
├── [RegionID] - [RegionName]/
│   ├── [ElectionName]/
│   │   ├── [ConstituencyName]/
│   │   │   ├── [ConstituencyID]/
│   │   │   │   ├── [ConstituencyID]_[Date]_[TimeRange]/
│   │   │   │   │   ├── [ConstituencyID]_[Date]_[TimeRange].csv
```

Example:
```
data/
├── 90 - Пермский край/
│   ├── Выборы депутатов Думы Красновишерского городского округа/
│   │   ├── Округ №1_3/
│   │   │   ├── AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM/
│   │   │   │   ├── AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900/
│   │   │   │   │   ├── AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900.csv
```

## Extracted Metadata

The system extracts the following metadata from the folder structure:

1. **Region Information**:
   - Region ID (e.g., "90")
   - Region Name (e.g., "Пермский край")

2. **Election Information**:
   - Election Name (e.g., "Выборы депутатов Думы Красновишерского городского округа")

3. **Constituency Information**:
   - Constituency Name (e.g., "Округ №1_3")
   - Constituency ID (e.g., "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM")

## Region Model

The system now includes a Region model to store region information:

```python
class Region(Base):
    """
    Region model for storing region information.
    
    Attributes:
        id (str): Region ID (e.g., "90")
        name (str): Region name (e.g., "Пермский край")
        country (str): Country name (default: "Russia")
    """
    
    __tablename__ = "regions"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False, default="Russia")
```

## Enhanced Schemas

The following schemas have been enhanced to include region, election, and constituency information:

### FileMetadata

```python
class FileMetadata:
    """
    Class for file metadata.
    
    This class represents metadata extracted from a file name and path.
    
    Attributes:
        constituency_id (str): ID of the constituency (smart contract address)
        date (date): Date of the data
        time_range (str): Time range of the data (e.g., "0800-0900")
        region_id (str, optional): ID of the region (e.g., "90")
        region_name (str, optional): Name of the region (e.g., "Пермский край")
        election_name (str, optional): Name of the election (e.g., "Выборы депутатов Думы Красновишерского городского округа")
        constituency_name (str, optional): Name of the constituency (e.g., "Округ №1_3")
    """
```

### ProcessingResult

```python
class ProcessingResult:
    """
    Class for file processing result.
    
    This class represents the result of processing a single file.
    
    Attributes:
        filename (str): Name of the processed file
        transactions_processed (int): Number of transactions processed
        constituency_id (str): ID of the constituency (smart contract address)
        date (date): Date of the data
        time_range (str): Time range of the data (e.g., "0800-0900")
        region_id (str, optional): ID of the region (e.g., "90")
        region_name (str, optional): Name of the region (e.g., "Пермский край")
        election_name (str, optional): Name of the election (e.g., "Выборы депутатов Думы Красновишерского городского округа")
        constituency_name (str, optional): Name of the constituency (e.g., "Округ №1_3")
    """
```

### DirectoryProcessingResult

```python
class DirectoryProcessingResult:
    """
    Class for directory processing result.
    
    This class represents the result of processing a directory of files.
    
    Attributes:
        files_processed (int): Number of files processed
        transactions_processed (int): Total number of transactions processed
        constituency_id (str): ID of the constituency (smart contract address)
        region_id (str, optional): ID of the region (e.g., "90")
        region_name (str, optional): Name of the region (e.g., "Пермский край")
        election_name (str, optional): Name of the election (e.g., "Выборы депутатов Думы Красновишерского городского округа")
        constituency_name (str, optional): Name of the constituency (e.g., "Округ №1_3")
    """
```

## Implementation Details

### FileService

The `FileService` class has been enhanced to extract metadata from folder paths:

```python
def extract_metadata_from_path(self, file_path: Path) -> Dict[str, str]:
    """
    Extract metadata from a file path.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Dictionary with extracted metadata (region_id, region_name, election_name, constituency_name, constituency_id)
        
    Raises:
        MetadataExtractionError: If metadata cannot be extracted
    """
```

### RegionService

The `RegionService` class provides methods for creating, updating, and retrieving regions:

```python
def create_or_update_region(self, region_id: str, region_name: str, country: str = "Russia") -> Region:
    """
    Create a new region or update an existing one.
    
    Args:
        region_id: Region ID
        region_name: Region name
        country: Country name (default: "Russia")
        
    Returns:
        Created or updated region
    """
```

```python
def extract_region_from_path(self, path_part: str) -> tuple:
    """
    Extract region ID and name from a path part.
    
    Args:
        path_part: Path part containing region information (e.g., "90 - Пермский край")
        
    Returns:
        Tuple of (region_id, region_name)
        
    Raises:
        ValueError: If the path part does not contain valid region information
    """
```

## Usage Examples

### Extracting Metadata from a File Path

```python
from app.services.file_service import FileService
from pathlib import Path

# Create a FileService instance
service = FileService()

# Extract metadata from a file path
file_path = Path("/path/to/data/90 - Пермский край/Выборы депутатов Думы Красновишерского городского округа/Округ №1_3/AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM/AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900/AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900.csv")
metadata = service.extract_metadata_from_path(file_path)

print(metadata)
# Output:
# {
#     "region_id": "90",
#     "region_name": "Пермский край",
#     "election_name": "Выборы депутатов Думы Красновишерского городского округа",
#     "constituency_name": "Округ №1_3",
#     "constituency_id": "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM"
# }
```

### Creating or Updating a Region

```python
from app.services.region_service import RegionService
from sqlalchemy.orm import Session

# Get a database session
db = Session()

# Create a RegionService instance
service = RegionService(db)

# Create or update a region
region = service.create_or_update_region("90", "Пермский край", "Russia")

print(region)
# Output:
# Region(id=90, name=Пермский край, country=Russia)
```

### Extracting Region Information from a Path Part

```python
from app.services.region_service import RegionService
from sqlalchemy.orm import Session

# Get a database session
db = Session()

# Create a RegionService instance
service = RegionService(db)

# Extract region information from a path part
region_id, region_name = service.extract_region_from_path("90 - Пермский край")

print(region_id, region_name)
# Output:
# 90 Пермский край
```

## Benefits

1. **Better Organization**: The system can now organize election data by region, election, and constituency.
2. **Enhanced Filtering**: Users can filter data by region, election, or constituency.
3. **Improved Reporting**: Reports can be generated for specific regions, elections, or constituencies.
4. **Data Integrity**: The system ensures that data is properly categorized and associated with the correct entities.
5. **Automatic Region Creation**: The system automatically creates or updates region information when processing files.