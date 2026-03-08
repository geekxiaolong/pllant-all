export default function ArchivedRootApp() {
  throw new Error(
    "[Archived root workspace] src/app/App.tsx belongs to the retired monolith root. Run the active apps from heart-plant/ or heart-plant-admin/ instead. See README.md and THREE-APP-DEPLOYMENT.md.",
  );
}
