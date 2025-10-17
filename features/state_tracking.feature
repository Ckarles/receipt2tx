Feature: Idempotency and Existing File Handling

  Background:
    Given a clean local storage destination
    And the application is configured to use the source "file://<SOURCE_PATH>"
    And the application is configured to store normalized files in "<DESTINATION_PATH>"

  # ----------------------------------------------------------------------------------
  # SCENARIO OUTLINE: Skip files that have already been converted
  # This uses the existence of the WEBP file as the "processed" marker
  # ----------------------------------------------------------------------------------
  Scenario Outline: Skip processing if the normalized file already exists
    Given the source storage contains an image file named "<SOURCE_FILENAME>"
    And the destination storage already contains the normalized file "<NORMALIZED_FILENAME>"
    And the local JSON data already contains an entry for "<SOURCE_FILENAME>"
    When the synchronization process is triggered
    Then the destination storage should still contain exactly one file named "<NORMALIZED_FILENAME>"
    And the log should indicate that "<SOURCE_FILENAME>" was skipped
    And the local JSON data should NOT have been updated for "<SOURCE_FILENAME>"

    Examples:
      | SOURCE_FILENAME | NORMALIZED_FILENAME |
      | receipt_03.png  | receipt_03.webp     |
      | document_04.pdf | document_04.webp    |

  # ----------------------------------------------------------------------------------
  # SCENARIO: Handle a corrupt or failed conversion
  # ----------------------------------------------------------------------------------
  Scenario: Log an error and do not save metadata on conversion failure
    Given the source storage contains an image file named "corrupt_image.jpg"
    When the synchronization process is triggered
    Then the destination storage should NOT contain a normalized file named "corrupt_image.webp"
    And an error should be logged for "corrupt_image.jpg" indicating conversion failure
    And the local JSON data should NOT contain any entry for "corrupt_image.jpg"
