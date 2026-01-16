/**
 * Utility function to extract error messages from API responses.
 * Handles the custom exception handler format from the backend.
 * 
 * Backend error format:
 * {
 *   "success": false,
 *   "error": {
 *     "code": "ERROR_CODE",
 *     "message": "Error message",
 *     "details": {} // optional
 *   }
 * }
 */
export const getErrorMessage = (error) => {
  if (!error) {
    return "An unknown error occurred";
  }

  // Handle axios error response
  if (error.response?.data) {
    const data = error.response.data;
    
    // Check for custom exception handler format
    if (data.error) {
      // Handle validation errors with details
      if (data.error.code === "VALIDATION_ERROR" && data.error.details) {
        const details = data.error.details;
        // Format validation errors in a user-friendly way
        const errorMessages = [];
        
        if (typeof details === "object" && !Array.isArray(details)) {
          Object.keys(details).forEach((field) => {
            const fieldErrors = Array.isArray(details[field])
              ? details[field]
              : [details[field]];
            fieldErrors.forEach((err) => {
              // Convert field names to readable format
              const readableField = field
                .replace(/_/g, " ")
                .replace(/\b\w/g, (l) => l.toUpperCase());
              errorMessages.push(`${readableField}: ${err}`);
            });
          });
        } else if (Array.isArray(details)) {
          errorMessages.push(...details);
        }
        
        return errorMessages.length > 0
          ? errorMessages.join(". ")
          : data.error.message || "Please check your input and try again";
      }
      
      // Return the error message from custom handler
      if (data.error.message) {
        return data.error.message;
      }
    }
    
    // Check for standard DRF error format
    if (data.detail) {
      return data.detail;
    }
    
    // Check for validation errors (array or object)
    if (Array.isArray(data)) {
      return data.join(", ");
    }
    
    if (typeof data === "object") {
      // Try to get first error message from object
      const firstKey = Object.keys(data)[0];
      if (firstKey && data[firstKey]) {
        if (Array.isArray(data[firstKey])) {
          const readableField = firstKey
            .replace(/_/g, " ")
            .replace(/\b\w/g, (l) => l.toUpperCase());
          return `${readableField}: ${data[firstKey][0]}`;
        }
        return `${firstKey}: ${data[firstKey]}`;
      }
    }
    
    // Fallback to string representation
    if (typeof data === "string") {
      return data;
    }
  }
  
  // Handle network errors
  if (error.message) {
    return error.message;
  }
  
  return "Failed to process request. Please try again later.";
};

export const getErrorCode = (error) => {
  if (error?.response?.data?.error?.code) {
    return error.response.data.error.code;
  }
  return null;
};

