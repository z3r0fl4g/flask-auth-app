import { ref, computed } from 'vue'

/**
 * Form validation composable extracted from Jinja2 login.html and signup.html templates
 * Provides email normalization, validation patterns, and dirty tracking
 */
export function useFormValidation() {
  // Validation patterns from Jinja2 templates
  const emailPattern = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/
  const passwordPattern = /^(?=.*[A-Za-z])(?=.*\d).{8,}$/
  const strongPasswordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{12,}$/

  /**
   * Normalize email address (lowercase domain)
   * @param {string} email - Email address to normalize
   * @returns {string} Normalized email
   */
  const normalizeEmail = (email) => {
    const trimmed = email.trim()
    if (!trimmed.includes('@')) return trimmed

    const [local, domain] = trimmed.split('@')
    return `${local}@${domain.toLowerCase()}`
  }

  /**
   * Validate email address
   * @param {string} email - Email to validate
   * @param {boolean} dirty - Whether the field has been touched
   * @param {boolean} attemptedSubmit - Whether form submission was attempted
   * @returns {object} Validation result
   */
  const validateEmail = (email, dirty = false, attemptedSubmit = false) => {
    const normalized = normalizeEmail(email)
    const valid = emailPattern.test(normalized)
    const showError = (dirty || attemptedSubmit) && !valid

    return {
      valid,
      normalized,
      showError,
      errorMessage: 'Please enter a valid email address'
    }
  }

  /**
   * Validate password strength
   * @param {string} password - Password to validate
   * @param {boolean} dirty - Whether the field has been touched
   * @param {boolean} attemptedSubmit - Whether form submission was attempted
   * @param {boolean} requireStrong - Whether to require strong password
   * @returns {object} Validation result
   */
  const validatePassword = (password, dirty = false, attemptedSubmit = false, requireStrong = false) => {
    const pattern = requireStrong ? strongPasswordPattern : passwordPattern
    const valid = pattern.test(password)
    const showError = (dirty || attemptedSubmit) && !valid

    let errorMessage = 'Password must be at least 8 characters with letter and number'
    if (requireStrong) {
      errorMessage = 'Password must be 12+ characters with uppercase, lowercase, number, and special character'
    }

    return {
      valid,
      showError,
      errorMessage
    }
  }

  /**
   * Validate password confirmation
   * @param {string} password - Original password
   * @param {string} confirmPassword - Confirmation password
   * @param {boolean} dirty - Whether the field has been touched
   * @param {boolean} attemptedSubmit - Whether form submission was attempted
   * @returns {object} Validation result
   */
  const validatePasswordConfirmation = (password, confirmPassword, dirty = false, attemptedSubmit = false) => {
    const valid = password === confirmPassword && confirmPassword.length > 0
    const showError = (dirty || attemptedSubmit) && !valid

    return {
      valid,
      showError,
      errorMessage: 'Passwords do not match'
    }
  }

  /**
   * Create a debounced validation function
   * @param {Function} validationFn - Validation function to debounce
   * @param {number} delay - Debounce delay in milliseconds (default 250ms from Jinja2 templates)
   * @returns {Function} Debounced validation function
   */
  const debounceValidation = (validationFn, delay = 250) => {
    let timeoutId = null

    return (...args) => {
      if (timeoutId) {
        clearTimeout(timeoutId)
      }

      return new Promise((resolve) => {
        timeoutId = setTimeout(() => {
          resolve(validationFn(...args))
        }, delay)
      })
    }
  }

  /**
   * Create form field state with dirty tracking
   * @param {any} initialValue - Initial field value
   * @returns {object} Field state
   */
  const createField = (initialValue = '') => {
    const value = ref(initialValue)
    const dirty = ref(false)
    const error = ref(null)

    const markDirty = () => {
      dirty.value = true
    }

    const reset = () => {
      value.value = initialValue
      dirty.value = false
      error.value = null
    }

    return {
      value,
      dirty,
      error,
      markDirty,
      reset
    }
  }

  return {
    // Patterns
    emailPattern,
    passwordPattern,
    strongPasswordPattern,

    // Functions
    normalizeEmail,
    validateEmail,
    validatePassword,
    validatePasswordConfirmation,
    debounceValidation,
    createField
  }
}
