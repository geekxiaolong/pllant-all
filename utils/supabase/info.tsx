export default function ArchivedRootModule() {
  throw new Error(
    "[Archived root workspace] This module belongs to the retired HeartPlant root monolith. Use heart-plant/, heart-plant-admin/, or heart-plant-api/ instead. See README.md and THREE-APP-DEPLOYMENT.md.",
  );
}
