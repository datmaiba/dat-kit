# HANDOFF 2026-07-24 — Execute PLAN v8 (refocus): start Phase A rename

## Goal

Thực thi `PLAN-v8-refocus.md` — cắt ngang phần dang dở của v7 để (1) đổi tên
`build-loop → code-loop` giữ alias, (2) thêm lệnh generic `task-loop` cho mọi việc
non-code, (3) sửa docs cho ranh giới rõ, rồi (4) **nối lại** telemetry-v3 + evolution
(KHÔNG park — north star "tool tự học, tự tiến hóa" giữ nguyên).

**Bắt đầu ở Phase A (đổi tên).** Mọi phase sau dựa trên tên mới ổn định.
Chưa được approve/execute — **plan-gated**: draft plan Phase A → `plan-reviewer` → STOP
chờ Dat duyệt trước mọi product edit.

## Điều kiện tiên quyết (làm TRƯỚC khi session khác chạy được)

`PLAN-v8-refocus.md` và handoff này hiện đang ở **scratchpad outputs của session này**,
KHÔNG nằm trong repo → session khác không đọc được. Trước khi hand off thật:
1. Commit `PLAN-v8-refocus.md` vào `plans/` (thay/để cạnh `PLAN-v7-platform.md`).
2. Commit handoff này vào `handoffs/`.
Cả hai cần Dat OK (quy ước no-drive-save) và có thể phải `del D:\project\dat-kit\.git\index.lock`
host-side nếu kẹt lock.

## Runtime (model theo `docs/model-selection.md` + PLAN §9)

- Controller session: tier cao nhất đang chơi.
- Phase A bulk rename (find-replace qua manifest/docs): **haiku**, nhưng verify alias bằng eval.
- Sửa descriptor `registry/domains.json` + render lại: **sonnet**.
- Reviewer (plan/qa/code/security): **opus** (pin sẵn — KHÔNG đổi pin, Class C).
- Không pin `fable`; chỉ raise per-dispatch nếu cần vượt opus.

## Workflow

`code-loop` (tức `build-loop` hiện tại — software-dev pack), attended, plan-gated.
Review order theo **PLAN §6 mới (thay v7 §9.1)**: Phase A là **tier B** (trigger đổi hành vi)
→ gate = `validate.py` + `render.py --check` byte-exact + trigger-eval pos/neg +
**eval alias** (test cả `code-loop` lẫn `build-loop`) + invoke thử. **Không** reviewer 3-agent
song song; reviewer tuần tự + diff-scoped nếu cần.

## Canonical contract

`dat-kit 1.16.0`. Đọc root `AGENTS.md` → `docs/agent-workflow.md`,
`docs/agent-working-rules.md`, `lessons-learned/lessons-learned.md` TRƯỚC.

## Git state (kỳ vọng lúc bắt đầu)

- Branch hiện tại: `feature/telemetry-v3-b3`, HEAD `f8cb45d` (B3 subset #3 done).
- Quyết định branch cho v8 rename: **cắt branch mới** `feature/v8-rename-code-loop` từ điểm
  green (không trộn vào telemetry branch). Xác nhận cây sạch (`git status`) trước khi bắt đầu.
- Telemetry/evolution resume point về sau: memory `dat-kit-b3-subset3-next` (subset #4).

## Rename surface — Phase A (điểm chạm, ĐỪNG bỏ sót — đây là chỗ rủi ro nhất)

Đổi qua descriptor → render, KHÔNG sửa tay file generated:
- `registry/domains.json` — trigger name `software-dev` = `code-loop`; thêm
  `aliases: ["build-loop"]`.
- Render lại → `skills/code-loop/SKILL.md`; giữ `skills/build-loop/SKILL.md` thành
  redirect/alias tối thiểu một minor.
- Host manifests: `.claude-plugin/plugin.json` + `marketplace.json`, `.codex-plugin/plugin.json`,
  `.agents/plugins/marketplace.json` — kiểm tra listing/skill name.
- `hooks.json` — kiểm tra tham chiếu tên nếu có.
- Skill `fable-dat` (`skills/fable-dat/`) — references `build-loop`; cập nhật + giữ alias.
- Docs: `README.md`, `HUONG_DAN.vi.md`, `docs/domains.md`, `docs/loops.md`,
  `docs/agent-workflow.md`, contracts — grep `build-loop` toàn repo.
- **Kiểm chứng:** `grep -rn "build-loop"` sau khi xong → chỉ còn ở chỗ alias/redirect có chủ ý.

## Bản đồ phase (toàn cảnh — chi tiết trong PLAN §4)

- **A** (giờ): rename `build-loop→code-loop` + alias. Tier B gate. haiku/sonnet.
- **B**: lệnh `task-loop` generated, registry-driven, loại trừ software-dev. Fixtures red-before-green.
- **C**: docs sweep + ranh giới code/non-code; gỡ "final/permanent".
- **D** (tùy chọn): author 1 non-code pack thật qua `domain-builder`.
- **E**: nối lại telemetry-v3 từ subset #4 (self-learning); ghi cả code lẫn non-code task.
- **F**: nối lại evolution `kit-evolve` (self-evolution); governed universe phủ cả task-loop.

## Decision log (đừng lật lại — Dat đã chốt 2026-07-24)

- GIỮ telemetry + evolution (không park, không xóa). Đảo lại đề xuất park ban đầu.
- Tên: `code-loop` (code) / `task-loop` (non-code); engine vẫn `work-loop`.
- Gate theo rủi ro (PLAN §6, 4 tier) thay chuỗi cứng v7 §9.1 cho việc maintain kit; full
  discipline chỉ còn bắt buộc cho tier D (evolution/enforcement code nới được gate).
- KHÔNG đổi reviewer `model:` pin (Class C, để dành evidence v2.1).

## Definition of Done — Phase A

- [ ] `code-loop` chạy y hệt `build-loop` cũ (software-dev pack, các mode không đổi).
- [ ] Alias `build-loop` vẫn kích hoạt; trigger-eval pass cho CẢ tên mới và alias.
- [ ] `render.py --check` byte-exact green; `validate.py` green.
- [ ] Mọi host manifest + docs + `fable-dat` nhất quán; `grep build-loop` chỉ còn alias có chủ ý.
- [ ] Một scorecard line cho Phase A.
- [ ] STOP tại plan-gate trước product edit; STOP để Dat duyệt trước khi merge.
