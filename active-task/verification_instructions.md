# File Processing System - Verification Instructions

This document provides instructions for verifying that the File Processing System implementation meets the requirements and works as expected. It includes test cases, expected outcomes, and verification steps.

## Verification Goals

1. Verify that the system can correctly extract metadata from file names
2. Verify that the system can parse CSV files and extract transactions
3. Verify that the system can process directories containing multiple files
4. Verify that the system handles errors gracefully
5. Verify that the API endpoints work as expected
6. Verify that the system updates constituency metrics correctly

## Prerequisites

Before starting verification, ensure that:

1. The implementation is complete according to the implementation plan
2. The database is set up and accessible
3. Sample data is available for testing
4. The application is running

## Test Cases

### 1. Metadata Extraction

**Test Case 1.1: Valid Filename**

- **Input**: `AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900.csv`
- **Expected Output**:
  - Constituency ID: `AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM`
  - Date: `2024-09-06`
  - Time Range: `0800-0900`

**Test Case 1.2: Invalid Filename**

- **Input**: `invalid_filename.csv`
- **Expected Output**: Error indicating invalid filename format

**Verification Steps**:
1. Create a test file with a valid filename
2. Call the `extract_metadata_from_filename` method
3. Verify that the extracted metadata matches the expected output
4. Create a test file with an invalid filename
5. Call the `extract_metadata_from_filename` method
6. Verify that an appropriate error is raised

### 2. CSV Parsing

**Test Case 2.1: Valid CSV File**

- **Input**: Sample CSV file from the data directory
- **Expected Output**: List of transactions with correct data

**Test Case 2.2: Invalid CSV File**

- **Input**: CSV file with missing or corrupt data
- **Expected Output**: Error indicating invalid CSV format or data

**Verification Steps**:
1. Select a sample CSV file from the data directory
2. Call the `extract_transactions_from_csv` method
3. Verify that the extracted transactions match the expected format and content
4. Create a test file with invalid CSV data
5. Call the `extract_transactions_from_csv` method
6. Verify that an appropriate error is raised

### 3. File Processing

**Test Case 3.1: Process Single File**

- **Input**: Sample CSV file from the data directory
- **Expected Output**: Processing result with correct statistics

**Test Case 3.2: Process Directory**

- **Input**: Directory containing multiple CSV files
- **Expected Output**: Processing result with correct statistics for all files

**Verification Steps**:
1. Select a sample CSV file from the data directory
2. Call the `process_file` method
3. Verify that the processing result matches the expected output
4. Select a directory containing multiple CSV files
5. Call the `process_directory` method
6. Verify that the processing result matches the expected output

### 4. Error Handling

**Test Case 4.1: File Not Found**

- **Input**: Non-existent file path
- **Expected Output**: Error indicating file not found

**Test Case 4.2: Permission Denied**

- **Input**: File with no read permission
- **Expected Output**: Error indicating permission denied

**Test Case 4.3: Invalid CSV Format**

- **Input**: File with invalid CSV format
- **Expected Output**: Error indicating invalid CSV format

**Verification Steps**:
1. Call the `process_file` method with a non-existent file path
2. Verify that an appropriate error is raised
3. Create a test file with no read permission
4. Call the `process_file` method
5. Verify that an appropriate error is raised
6. Create a test file with invalid CSV format
7. Call the `process_file` method
8. Verify that an appropriate error is raised

### 5. API Endpoints

**Test Case 5.1: Upload Valid File**

- **Input**: Sample CSV file from the data directory
- **Expected Output**: Success response with processing statistics

**Test Case 5.2: Upload Invalid File**

- **Input**: File with invalid format or data
- **Expected Output**: Error response with appropriate message

**Test Case 5.3: Process Valid Directory**

- **Input**: Directory containing multiple CSV files
- **Expected Output**: Success response with processing statistics

**Test Case 5.4: Process Invalid Directory**

- **Input**: Non-existent or empty directory
- **Expected Output**: Error response with appropriate message

**Verification Steps**:
1. Use a tool like curl or Postman to send a POST request to the `/api/files/upload` endpoint with a valid CSV file
2. Verify that the response matches the expected output
3. Send a POST request with an invalid file
4. Verify that the response matches the expected output
5. Send a POST request to the `/api/files/process-directory` endpoint with a valid directory path
6. Verify that the response matches the expected output
7. Send a POST request with an invalid directory path
8. Verify that the response matches the expected output

### 6. Constituency Metrics Update

**Test Case 6.1: Update Metrics After Processing**

- **Input**: Sample CSV file with transaction data
- **Expected Output**: Updated constituency metrics in the database

**Verification Steps**:
1. Check the current metrics for a constituency in the database
2. Process a sample CSV file for that constituency
3. Check the metrics again
4. Verify that the metrics have been updated correctly based on the transactions in the file

## Integration Testing

### Test Case I.1: End-to-End File Upload and Processing

- **Input**: Sample CSV file from the data directory
- **Expected Output**: 
  - Success response from the API
  - Transactions stored in the database
  - Updated constituency metrics

**Verification Steps**:
1. Check the current state of the database (transaction count, constituency metrics)
2. Use a tool like curl or Postman to send a POST request to the `/api/files/upload` endpoint with a valid CSV file
3. Verify that the response indicates success
4. Check the database again
5. Verify that new transactions have been added
6. Verify that constituency metrics have been updated

### Test Case I.2: End-to-End Directory Processing

- **Input**: Directory containing multiple CSV files
- **Expected Output**: 
  - Success response from the API
  - Transactions from all files stored in the database
  - Updated constituency metrics

**Verification Steps**:
1. Check the current state of the database (transaction count, constituency metrics)
2. Use a tool like curl or Postman to send a POST request to the `/api/files/process-directory` endpoint with a valid directory path
3. Verify that the response indicates success
4. Check the database again
5. Verify that new transactions have been added from all files
6. Verify that constituency metrics have been updated

## Performance Testing

### Test Case P.1: Large File Processing

- **Input**: Large CSV file (e.g., 1000+ transactions)
- **Expected Output**: Successful processing without memory issues

**Verification Steps**:
1. Create or obtain a large CSV file
2. Process the file using the API
3. Monitor memory usage during processing
4. Verify that the file is processed successfully
5. Verify that memory usage remains within acceptable limits

### Test Case P.2: Multiple File Processing

- **Input**: Directory with many CSV files
- **Expected Output**: Successful processing of all files within a reasonable time

**Verification Steps**:
1. Create or obtain a directory with many CSV files
2. Process the directory using the API
3. Monitor processing time
4. Verify that all files are processed successfully
5. Verify that processing time is within acceptable limits

## Verification Checklist

Use this checklist to ensure that all aspects of the system have been verified:

- [ ] Metadata extraction works correctly for valid filenames
- [ ] Metadata extraction handles invalid filenames gracefully
- [ ] CSV parsing works correctly for valid CSV files
- [ ] CSV parsing handles invalid CSV files gracefully
- [ ] File processing works correctly for single files
- [ ] Directory processing works correctly for multiple files
- [ ] Error handling works correctly for various error cases
- [ ] API endpoints return correct responses for valid inputs
- [ ] API endpoints return appropriate error messages for invalid inputs
- [ ] Constituency metrics are updated correctly after processing
- [ ] End-to-end file upload and processing works correctly
- [ ] End-to-end directory processing works correctly
- [ ] Large file processing works without memory issues
- [ ] Multiple file processing works within a reasonable time

## Troubleshooting

If verification fails, consider the following troubleshooting steps:

1. **Metadata Extraction Issues**:
   - Check the filename format
   - Verify that the regex patterns in the validators are correct
   - Check for encoding issues in the filename

2. **CSV Parsing Issues**:
   - Check the CSV format
   - Verify that the file is properly encoded (UTF-8)
   - Check for special characters or line breaks in the data

3. **File Processing Issues**:
   - Check file permissions
   - Verify that the file path is correct
   - Check for disk space issues

4. **API Issues**:
   - Check that the API server is running
   - Verify that the request format is correct
   - Check for network issues

5. **Database Issues**:
   - Check the database connection
   - Verify that the database schema is correct
   - Check for transaction conflicts or locks

## Conclusion

By following these verification instructions, you can ensure that the File Processing System implementation meets the requirements and works as expected. If all test cases pass, the system is ready for deployment.