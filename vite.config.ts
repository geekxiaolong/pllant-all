import { defineConfig } from 'vite'

export default defineConfig(() => {
  throw new Error(
    'Archived root workspace: this repository root no longer serves the HeartPlant monolith. Use ./heart-plant, ./heart-plant-admin, or ./heart-plant-api instead. See README.md / START_HERE.md / THREE-APP-DEPLOYMENT.md.',
  )
})
