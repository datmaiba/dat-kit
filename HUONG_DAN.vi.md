# dat-kit — Hướng dẫn tiếng Việt

Toolkit phát triển phần mềm spec-driven cho Claude Code và Codex. Cài 1 lệnh, agent có ngay kỷ luật làm việc trọn bộ: nghĩ trước khi code, plan trước khi build, verify trước khi báo xong, đúc kết bài học sau khi ship.

## Cài đặt

```
/plugin marketplace add datmaiba/dat-kit
/plugin install dat-kit@dat-kit
```

Dev/test local từ folder: `claude --plugin-dir /đường/dẫn/dat-kit`

**Codex:**

```bash
codex plugin marketplace add datmaiba/dat-kit
codex plugin add dat-kit@dat-kit
```

Xem [docs/codex.md](docs/codex.md) để biết giới hạn theo host: mọi runtime dùng `AGENTS.md` canonical, Codex chưa parse token transcript và không dùng Claude SessionStart hook.

## Có gì bên trong

| Thành phần | Công dụng |
|---|---|
| `/dat-kit:project-init` | Scaffold project mới (hoặc `--here` cho repo sẵn có): `AGENTS.md` canonical + pointer adapters, skeleton `spec/00→08`, shared agent docs, lessons-learned + `CONTEXT.md` |
| `/dat-kit:build-loop` | Vòng lặp build: load context → tự chất vấn theo spec → plan → **chờ duyệt** → build → chạy gates → review độc lập → đúc kết bài học. Autopilot: PREFLIGHT gom mọi câu hỏi thành 1 lần duyệt duy nhất. Delegated-build ("delegated build"): session chính làm orchestrator, mỗi task 1 builder subagent mới + review 2 bước (đúng spec → chất lượng code) |
| `/dat-kit:handoff` | Nén session đang dở thành file bàn giao trong `handoffs/` — session mới (hoặc máy khác) đọc là tiếp tục được ngay; build-loop recovery tự đọc file mới nhất |
| `/dat-kit:fable-mode` | Kỷ luật làm việc kiểu Fable với 3 mức effort (low/medium/high) |
| `/dat-kit:fable-pro` | Bản cho mọi ngành nghề ngoài code (kế toán, luật, design, y...) |
| `/dat-kit:guardian-builder` | Sinh "guardian" riêng cho 1 repo: checklist bắt buộc trước khi code, chưng cất từ convention thật + lessons-learned của repo đó |
| `/dat-kit:scorecard` | Chấm điểm task: rubric độ phức tạp 1-5 cố định, ước lượng giờ-tay tiết kiệm (dán nhãn estimate), thời gian thật, gates — ghi vào `benchmarks/scorecard.jsonl`. Chạy `python3 scripts/scorecard.py` để điền token THẬT từ transcript Claude Code + in bảng tổng hợp. Build-loop tự gọi cuối mỗi phase |
| 4 agents | `plan-reviewer`, `qa-agent`, `code-reviewer`, `security-reviewer` — builder không bao giờ tự chấm bài mình |
| SessionStart hook | Tự inject kỷ luật làm việc vào đầu mọi session — không cần gọi skill tay |
| `scripts/statusline.py` | Hiện token sau MỖI câu lệnh trên statusline Claude Code: `turn in/out · session total · ~cost · ctx %`. Setup 1 lần mỗi máy: `python3 scripts/statusline.py --install` rồi restart Claude Code (chỉ có trong Claude Code, Cursor không có statusline) |

## Dùng hằng ngày

**Project mới:**

```
/dat-kit:project-init          → trả lời tên/mô tả/stack → có skeleton
(điền spec/ theo thứ tự 00 → 04, quan trọng nhất là non-goals và build phases)
/dat-kit:build-loop phase 0    → hoặc: "run build-loop autopilot from phase 0"
```

**Repo sẵn có:** `bash scripts/init.sh --here` (không bao giờ ghi đè file đang có), rồi `/dat-kit:guardian-builder` để sinh rules riêng từ convention thật của repo.

## Nguyên tắc cốt lõi

- **Spec là luật** — agent tự trả lời câu hỏi từ spec (kèm citation), chỉ hỏi user cái spec không trả lời được.
- **1 điểm duyệt duy nhất** — PREFLIGHT gom hết quyết định lên đầu, ghi vào `spec/08-decisions.md`; autopilot chỉ dừng cho câu hỏi high-severity (secrets, xoá data, lệch spec, tốn tiền, public contract).
- **Review độc lập** — subagent tươi audit plan, tấn công feature bằng edge case, soi diff.
- **Bằng chứng thay lời hứa** — phase chưa xanh gates + demo chưa chạy = chưa xong; báo cáo ghi kết quả cụ thể ("pest 24/24 ✓"), cấm "mọi thứ đều ổn".
- **Bài học cộng dồn** — mỗi lần bị sửa thành 1 entry lessons-learned mà session sau bắt buộc đọc.

## Bảo trì

### Quy trình update plugin (làm đúng thứ tự, mỗi lần sửa bất kỳ thứ gì)

1. Sửa file (skill/agent/template/script/hook)
2. `python scripts/validate.py` — phải "all checks green" (đúng bộ check CI chạy)
3. Bump version ở BA manifest: `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`; chỉ sửa `.agents/plugins/marketplace.json` khi source metadata đổi. Patch (`x.y.Z`) cho fix, minor (`x.Y.0`) cho tính năng mới
4. `git add -A && git commit && git push` — check tab Actions trên GitHub phải xanh
5. Trong Claude Code: `/plugin` → Marketplaces → update dat-kit → tab Installed hiện version mới (bước này bắt buộc làm tay — model không tự chạy được lệnh UI, và đây là chốt bảo mật có chủ đích)
6. Mở session MỚI — session đang chạy vẫn dùng bản cũ đã nạp lúc khởi động (hoặc `/reload-plugins` nếu chỉ cần hook/agent)

**Nguyên tắc thứ tự**: sửa tool trước, dùng tool sau — thay đổi dat-kit rẻ (1 file, 1 push), phase build thì đắt; đừng chạy phase dài trên tool có bug đã biết.

### Thêm stack profile mới

Tạo `templates/profiles/<tên>/` với 3 file `architecture.md`, `gates.md`, `traps.md` — chỉ thêm khi đã thực chiến stack đó, đừng viết chay.

## Adopt repo brownfield an toàn

`bash scripts/init.sh --here` cần Python và chạy preflight read-only trước mọi
`mkdir`, copy hay sửa file. Nếu có `AGENTS.md` cạnh tranh, pointer chứa policy,
contract legacy, symlink không an toàn, hoặc partial install không tương thích,
script trả diagnostic có tên và dừng mà không đổi cây thư mục. v1.16.0 chỉ hỗ
trợ migration thủ công; xem `docs/codex.md`, hợp nhất policy vào contract
canonical rồi chạy lại `python scripts/contract_check.py --target .`.

Cam kết không drift chỉ áp dụng cho installation đã pass checker. Plugin đã cài
và session đang mở vẫn giữ metadata cũ cho đến khi update/reinstall và mở session
mới.
