Feature: Image Synchronization and Conversion Pipeline

  Background:
    Given a clean local storage destination
    And the application is configured to use the source "file://<SOURCE_PATH>"
    And the application is configured to store normalized files in "<DESTINATION_PATH>"

  # ----------------------------------------------------------------------------------
  # SCENARIO 1: Successfully process a new image file and convert it
  # ----------------------------------------------------------------------------------
  Scenario: Successfully process a new image file and convert to WebP
    Given the source storage contains a new image file named "receipt_01.jpg"
    When the synchronization process is triggered
    Then the destination storage should contain a normalized file named "receipt_01.webp"
    And the checksum for "receipt_01.jpg" should be recorded in the local JSON data
    And the path to "receipt_01.webp" should be recorded in the local JSON data

  # ----------------------------------------------------------------------------------
  # SCENARIO 2: Handle a PDF file (which should also be converted/processed)
  # ----------------------------------------------------------------------------------
  Scenario: Successfully process a new PDF file
    Given the source storage contains a new file named "document_02.pdf"
    When the synchronization process is triggered
    Then the destination storage should contain a normalized file named "document_02.webp"
    And the checksum for "document_02.pdf" should be recorded in the local JSON data

  # ----------------------------------------------------------------------------------
  # SCENARIO 3: Skip processing for files that are not valid image/document formats
  # (Assuming your application filters out non-image/non-pdf files)
  # ----------------------------------------------------------------------------------
  Scenario: Skip non-image/non-PDF files and log an error
    Given the source storage contains an invalid file named "data.txt"
    When the synchronization process is triggered
    Then the destination storage should NOT contain a file named "data.txt"
    And an error should be logged for "data.txt"
    And the local JSON data should NOT contain any entry for "data.txt"
