# dat-kit — Hướng dẫn tiếng Việt

Toolkit phát triển phần mềm spec-driven cho Claude Code. Cài 1 lệnh, agent có ngay kỷ luật làm việc trọn bộ: nghĩ trước khi code, plan trước khi build, verify trước khi báo xong, đúc kết bài học sau khi ship.

## Cài đặt

```
/plugin marketplace add datmaiba/dat-kit
/plugin install dat-kit@dat-kit
```

Dev/test local từ folder: `claude --plugin-dir /đường/dẫn/dat-kit`

## Có gì bên trong

| Thành phần | Công dụng |
|---|---|
| `/dat-kit:project-init` | Scaffold project mới (hoặc `--here` cho repo sẵn có): CLAUDE.md ghép từ stack profile + skeleton `spec/00→08` + rules + lessons-learned |
| `/dat-kit:build-loop` | Vòng lặp build: load context → tự chất vấn theo spec → plan → **chờ duyệt** → build → chạy gates → review độc lập → đúc kết bài học. Autopilot: PREFLIGHT gom mọi câu hỏi thành 1 lần duyệt duy nhất |
| `/dat-kit:fable-mode` | Kỷ luật làm việc kiểu Fable với 3 mức effort (low/medium/high) |
| `/dat-kit:fable-pro` | Bản cho mọi ngành nghề ngoài code (kế toán, luật, design, y...) |
| `/dat-kit:guardian-builder` | Sinh "guardian" riêng cho 1 repo: checklist bắt buộc trước khi code, chưng cất từ convention thật + lessons-learned của repo đó |
| `/dat-kit:scorecard` | Chấm điểm task: rubric độ phức tạp 1-5 cố định, ước lượng giờ-tay tiết kiệm (dán nhãn estimate), thời gian thật, gates — ghi vào `benchmarks/scorecard.jsonl`. Chạy `python3 scripts/scorecard.py` để điền token THẬT từ transcript Claude Code + in bảng tổng hợp. Build-loop tự gọi cuối mỗi phase |
| 3 agents | `plan-reviewer`, `qa-agent`, `code-reviewer` — builder không bao giờ tự chấm bài mình |
| SessionStart hook | Tự inject kỷ luật làm việc vào đầu mọi session — không cần gọi skill tay |

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

Sửa gì cũng phải: chạy `python3 scripts/validate.py` (đúng bộ check CI chạy trên GitHub) + **bump version** ở cả `plugin.json` và `marketplace.json` (không bump = user không nhận update). Thêm stack profile mới: tạo folder `templates/profiles/<tên>/` với 3 file `architecture.md`, `gates.md`, `traps.md` — chỉ thêm khi đã thực chiến stack đó, đừng viết chay.
