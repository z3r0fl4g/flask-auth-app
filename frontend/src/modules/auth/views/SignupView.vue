<template>
  <div class="min-h-[calc(100vh-72px)] grid lg:grid-cols-2">
    <!-- Left: Form Section -->
    <section
      class="bg-white flex items-center justify-center px-4 py-12 lg:px-8"
    >
      <div class="w-full max-w-sm">
        <!-- Header -->
        <div class="text-center mb-6">
          <h1 class="text-xl font-semibold text-gray-900">
            Create your account
          </h1>
          <p class="text-sm text-gray-500 mt-1">
            Join the Haitian event community
          </p>
        </div>

        <!-- Error Message -->
        <div
          v-if="authStore.error"
          class="mb-4 rounded-xl bg-rose-50 border border-rose-100 px-3 py-2 text-sm text-rose-600"
        >
          {{ authStore.error }}
        </div>

        <form @submit.prevent="handleSignup" class="space-y-4">
          <!-- Full Name -->
          <div>
            <label
              for="fullname"
              class="block text-sm font-medium text-gray-700 mb-1.5"
            >
              Full Name
            </label>
            <input
              id="fullname"
              v-model="fullnameField.value.value"
              type="text"
              placeholder="John Doe"
              required
              autocomplete="name"
              class="w-full px-3 py-2.5 rounded-xl border border-gray-200 text-sm text-gray-900 placeholder:text-gray-400 focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20 outline-none transition"
              @blur="fullnameField.markDirty()"
            />
          </div>

          <!-- Email -->
          <div>
            <label
              for="email"
              class="block text-sm font-medium text-gray-700 mb-1.5"
            >
              Email
            </label>
            <input
              id="email"
              v-model="emailField.value.value"
              type="email"
              placeholder="you@example.com"
              required
              autocomplete="email"
              class="w-full px-3 py-2.5 rounded-xl border border-gray-200 text-sm text-gray-900 placeholder:text-gray-400 focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20 outline-none transition"
              :class="{ 'border-rose-400': emailField.error.value }"
              @blur="validateEmailField"
            />
            <p v-if="emailField.error.value" class="mt-1 text-xs text-rose-500">
              {{ emailField.error.value }}
            </p>
          </div>

          <!-- Password -->
          <div>
            <label
              for="password"
              class="block text-sm font-medium text-gray-700 mb-1.5"
            >
              Password
            </label>
            <div class="relative">
              <input
                id="password"
                v-model="passwordField.value.value"
                :type="showPassword ? 'text' : 'password'"
                placeholder="••••••••"
                required
                autocomplete="new-password"
                class="w-full px-3 py-2.5 pr-10 rounded-xl border border-gray-200 text-sm text-gray-900 placeholder:text-gray-400 focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20 outline-none transition"
                :class="{ 'border-rose-400': passwordField.error.value }"
                @blur="validatePasswordField"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <svg
                  v-if="!showPassword"
                  class="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                  />
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                  />
                </svg>
                <svg
                  v-else
                  class="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
                  />
                </svg>
              </button>
            </div>
            <p
              v-if="passwordField.error.value"
              class="mt-1 text-xs text-rose-500"
            >
              {{ passwordField.error.value }}
            </p>
            <p v-else class="mt-1 text-xs text-gray-400">
              8+ characters with letters and numbers
            </p>
          </div>

          <!-- Submit -->
          <button
            type="submit"
            :disabled="authStore.loading || !isFormValid"
            class="btn-primary w-full justify-center"
          >
            {{ authStore.loading ? "Creating account..." : "Create account" }}
          </button>
        </form>

        <!-- Divider -->
        <div class="relative my-5">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-200"></div>
          </div>
          <div class="relative flex justify-center">
            <span class="bg-white px-3 text-xs text-gray-400">or</span>
          </div>
        </div>

        <!-- Google OAuth -->
        <a
          href="/auth/login/google"
          class="flex items-center justify-center gap-2 w-full py-2.5 rounded-xl border border-gray-200 text-sm font-medium text-gray-700 hover:bg-gray-50 transition"
        >
          <svg class="w-4 h-4" viewBox="0 0 24 24">
            <path
              fill="#4285F4"
              d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
            />
            <path
              fill="#34A853"
              d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
            />
            <path
              fill="#FBBC05"
              d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
            />
            <path
              fill="#EA4335"
              d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
            />
          </svg>
          Continue with Google
        </a>

        <!-- Login link -->
        <p class="mt-5 text-center text-sm text-gray-500">
          Already have an account?
          <router-link
            to="/login"
            class="font-medium text-violet-600 hover:text-violet-700"
          >
            Sign in
          </router-link>
        </p>

        <!-- Terms -->
        <p class="mt-4 text-center text-xs text-gray-400">
          By signing up, you agree to our
          <a href="/terms" class="text-gray-500 hover:text-gray-700">Terms</a>
          and
          <a href="/privacy" class="text-gray-500 hover:text-gray-700"
            >Privacy Policy</a
          >.
        </p>
      </div>
    </section>

    <!-- Right: Visual Section (hidden on mobile) -->
    <section
      class="hidden lg:flex items-center justify-center bg-gradient-to-br from-violet-600 via-violet-700 to-indigo-800 relative overflow-hidden"
    >
      <!-- Background Pattern -->
      <div class="absolute inset-0 opacity-10">
        <svg
          class="w-full h-full"
          viewBox="0 0 100 100"
          preserveAspectRatio="none"
        >
          <defs>
            <pattern
              id="grid"
              width="10"
              height="10"
              patternUnits="userSpaceOnUse"
            >
              <circle cx="1" cy="1" r="1" fill="white" />
            </pattern>
          </defs>
          <rect width="100" height="100" fill="url(#grid)" />
        </svg>
      </div>

      <!-- Content -->
      <div class="relative z-10 max-w-md px-8 text-center">
        <!-- Icon -->
        <div
          class="w-20 h-20 mx-auto mb-8 rounded-2xl bg-white/10 backdrop-blur flex items-center justify-center"
        >
          <svg
            class="w-10 h-10 text-white"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1.5"
              d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z"
            />
          </svg>
        </div>

        <h2 class="text-3xl font-bold text-white mb-4">
          Discover Haitian Events
        </h2>
        <p class="text-violet-100 text-lg leading-relaxed">
          From Kompa nights in Brooklyn to Rara parades in Miami — find verified
          events and secure your tickets instantly.
        </p>

        <!-- Stats -->
        <div class="mt-10 flex justify-center gap-8">
          <div class="text-center">
            <div class="text-2xl font-bold text-white">10K+</div>
            <div class="text-sm text-violet-200">Events</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-white">50+</div>
            <div class="text-sm text-violet-200">Cities</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-white">100%</div>
            <div class="text-sm text-violet-200">Verified</div>
          </div>
        </div>
      </div>

      <!-- Decorative elements -->
      <div
        class="absolute -bottom-20 -left-20 w-64 h-64 bg-white/5 rounded-full blur-3xl"
      ></div>
      <div
        class="absolute -top-20 -right-20 w-80 h-80 bg-indigo-500/20 rounded-full blur-3xl"
      ></div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useFormValidation } from "../composables/useFormValidation";
import OAuth2Buttons from "../components/OAuth2Buttons.vue";

const router = useRouter();
const authStore = useAuthStore();
const { validateEmail, validatePassword, createField } = useFormValidation();

const fullnameField = createField("");
const emailField = createField("");
const passwordField = createField("");
const showPassword = ref(false);
const attemptedSubmit = ref(false);

// Clear any existing errors when the page loads
onMounted(() => {
  authStore.clearError();
});

const isFormValid = computed(() => {
  return (
    fullnameField.value.value.length > 0 &&
    emailField.value.value.length > 0 &&
    passwordField.value.value.length > 0
  );
});

function validateEmailField() {
  emailField.markDirty();
  const result = validateEmail(
    emailField.value.value,
    emailField.dirty.value,
    attemptedSubmit.value,
  );
  emailField.error.value = result.showError ? result.errorMessage : null;
}

function validatePasswordField() {
  passwordField.markDirty();
  const result = validatePassword(
    passwordField.value.value,
    passwordField.dirty.value,
    attemptedSubmit.value,
  );
  passwordField.error.value = result.showError ? result.errorMessage : null;
}

async function handleSignup() {
  attemptedSubmit.value = true;
  validateEmailField();
  validatePasswordField();

  if (emailField.error.value || passwordField.error.value) {
    return;
  }

  try {
    const result = await authStore.signup(
      emailField.value.value,
      passwordField.value.value,
      fullnameField.value.value,
    );
    if (result.requires2FA) {
      router.push("/2fa/verify");
    } else {
      router.push("/profile");
    }
  } catch (error) {
    // Error handled in store
  }
}
</script>
