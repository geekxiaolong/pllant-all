# 子仓库说明（Submodules）

本仓库通过 Git Submodule 关联三个子项目：

| 路径 | 仓库 | 说明 |
|------|------|------|
| `heart-plant` | [geekxiaolong/heart-plant](https://github.com/geekxiaolong/heart-plant) | 用户端前端 |
| `heart-plant-admin` | [geekxiaolong/heart-plant-admin](https://github.com/geekxiaolong/heart-plant-admin) | 管理端前端 |
| `heart-plant-api` | [geekxiaolong/heart-plant-api](https://github.com/geekxiaolong/heart-plant-api) | 后端 API |

## 首次克隆本仓库时

```bash
git clone --recurse-submodules https://github.com/geekxiaolong/pllant-all.git
# 或已克隆后补拉子模块：
git submodule update --init --recursive
```

## 日常更新子模块到各自远程最新

```bash
git submodule update --remote --merge
```

## 在子模块里改代码

```bash
cd heart-plant   # 或 heart-plant-admin / heart-plant-api
git checkout main
# 修改、提交、推送
git add . && git commit -m "..." && git push origin main
# 回到父仓库，记录新的子模块提交
cd ..
git add heart-plant && git commit -m "chore: 更新 heart-plant 子模块"
git push
```

## 一键启动三服务（需先拉齐子模块）

```bash
./start-all.sh
```

（脚本会启动 API、管理端、用户端三个服务。）
