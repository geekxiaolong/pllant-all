#!/usr/bin/env node
/**
 * 使用管理员账号登录并调用接口，将指定账号下「品种错误」的植物统一改为默认品种（默认向日葵）。
 * 用法：EMAIL=776427024@qq.com PASSWORD=你的密码 node scripts/fix-user-plant-species.mjs
 * 或：npx node scripts/fix-user-plant-species.mjs
 * 环境变量：EMAIL, PASSWORD（可选，不填则用下方默认）；API_BASE（可选，默认 Supabase 云函数）
 */

import { createClient } from "@supabase/supabase-js";

const SUPABASE_URL = process.env.SUPABASE_URL || "https://dkszigraljeptpeiimzg.supabase.co";
const SUPABASE_ANON_KEY =
  process.env.SUPABASE_ANON_KEY ||
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRrc3ppZ3JhbGplcHRwZWlpbXpnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI0MjkyMDEsImV4cCI6MjA4ODAwNTIwMX0.piPkMGZDQ6O4l-YhZwPIU-Fp5Q-UUwt5fwvYlKVu6x0";
const API_BASE =
  process.env.API_BASE ||
  `${SUPABASE_URL}/functions/v1/make-server-4b732228`;

const EMAIL = process.env.EMAIL || "776427024@qq.com";
const PASSWORD = process.env.PASSWORD || "1357655";

async function main() {
  if (!PASSWORD) {
    console.error("请设置环境变量 PASSWORD，或使用默认密码（仅限本地排查）");
    process.exit(1);
  }
  const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
  console.log("登录账号:", EMAIL);
  const {
    data: { session },
    error: authError,
  } = await supabase.auth.signInWithPassword({
    email: EMAIL,
    password: PASSWORD,
  });
  if (authError) {
    console.error("登录失败:", authError.message);
    process.exit(1);
  }
  if (!session?.access_token) {
    console.error("未获取到 access_token");
    process.exit(1);
  }
  console.log("登录成功，正在调用修复接口...");
  const url = `${API_BASE}/admin/fix-user-plant-species`;
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${session.access_token}`,
    },
    body: JSON.stringify({
      email: EMAIL,
      defaultSpecies: "向日葵",
    }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    console.error("接口请求失败:", res.status, data);
    process.exit(1);
  }
  console.log("结果:", JSON.stringify(data, null, 2));
  if (data.report?.length) {
    console.log("\n已修正的植物:");
    data.report.forEach((r) =>
      console.log(`  - ${r.id}  名称:${r.name}  原品种:${r.species}  原因:${r.reason}`)
    );
  }
  console.log("\n已将该账号下品种错误的植物统一改为: 向日葵, 共", data.fixed, "条");
}

main();
