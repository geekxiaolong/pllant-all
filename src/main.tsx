const root = document.getElementById('root');

if (root) {
  root.innerHTML = `
    <main style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; padding: 40px; line-height: 1.6; color: #111827;">
      <h1 style="margin: 0 0 16px; font-size: 28px;">Archived root workspace</h1>
      <p style="margin: 0 0 12px;">当前根目录仅保留历史归档与导航，不再作为 HeartPlant 单体前端入口。</p>
      <p style="margin: 0;">请改用 <code>heart-plant/</code>、<code>heart-plant-admin/</code>、<code>heart-plant-api/</code> 三个独立仓库，并参考 <code>THREE-APP-DEPLOYMENT.md</code>。</p>
    </main>
  `;
} else {
  throw new Error('Archived root workspace: missing #root container');
}
