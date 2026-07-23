# dat-kit — Plan v8: Refocus (tách lệnh code / non-code; giữ hướng tự tiến hóa)

**Status:** ĐỀ XUẤT — chờ Dat duyệt. Cắt ngang `PLAN-v7-platform.md` để **chèn** workstream
tách lệnh lên trước, rồi **nối lại** telemetry-v3 và evolution (KHÔNG park).
**Ngày:** 2026-07-24
**Neo vào:** mục tiêu ban đầu — *"open discipline platform mà tâm điểm ổn định là một work
contract, không phải một coding agent"* — và **north star giữ nguyên: kit tự học từ lịch sử
và tự đề xuất cải tiến chính nó** (v7 §1.5, §3.11, Phase 7).
**Không đụng:** engine, 6-slot Domain Packs, registry/projections, hai pack đang có, release
v2.0.

---

## 0. Vì sao cắt ngang (và vì sao KHÔNG park)

Ba tầng nền (engine + domain packs + registry) đã ship và green — giữ nguyên. Hai khối v7
còn dở là **telemetry-v3** (đo I/O, gate, review theo thời gian) và **evolution engine**
(`kit-evolve` sinh proposal cải tiến) — đây chính là bộ máy hiện thực hóa "tool tự học, tự
tiến hóa", nên **vẫn nằm trong lộ trình**, không park.

Điều cần sửa *ngay* là **UX phân định code vs non-code**, và nó gần như đã sẵn ở tầng kiến
trúc: trigger `build-loop` chỉ load pack `software-dev`; `knowledge-work` đã là pack riêng.
Thứ thiếu là: (a) một **entry point rõ ràng cho mọi việc non-code**, (b) **đổi tên** cho ranh
giới hiển nhiên, (c) docs nhất quán.

**Thứ tự hợp lý:** làm workstream tách lệnh + đổi tên TRƯỚC (nhỏ, đụng trigger/registry),
rồi mới nối lại telemetry B-line + evolution — vì đổi tên xong trước sẽ tránh churn cho phần
telemetry vốn cũng chạm các trigger/producer đó.

**Luận điểm giữ nguyên:** một lệnh generic `task-loop` route qua registry tới mọi non-software
pack là biểu hiện thật của open-platform — pack mới (qua `domain-builder`) tự xuất hiện, không
cần viết skill mới; và mỗi pack đó cũng là một component nằm trong "governed universe" mà
`kit-evolve` sau này có thể đề xuất cải tiến. Tách lệnh và tự-tiến-hóa **bổ trợ nhau**, không
mâu thuẫn.

## 1. Ba quyết định chốt

| # | Câu hỏi | Quyết định | Ghi chú |
|---|---|---|---|
| Q1 | telemetry-v3 / evolution? | **CONTINUE** — giữ north star tự tiến hóa; chỉ **hoãn** sau workstream tách lệnh | Không park, không xóa |
| Q2 | tên lệnh? | **`code-loop`** (đổi từ `build-loop`) cho code · **`task-loop`** cho non-code | Cặp `-loop` song song; engine vẫn là *work-loop* |
| Q3 | mức thay đổi? | Đổi tên + thêm `task-loop` + docs, **giữ** registry/telemetry/evolution | Rip = không |

### Bản đồ tên
- **work-loop engine** (`engine/work-loop/`) — máy phase host-neutral, không đổi.
- **`code-loop`** — trigger cho pack `software-dev` (đổi tên từ `build-loop`, giữ alias).
- **`task-loop`** — trigger generic route tới mọi non-software active pack.

## 2. Non-negotiables (giữ từ v7)

1. Một policy owner cho generated project: `AGENTS.md`.
2. Một descriptor owner mỗi component; skill trigger là projection byte-exact từ registry.
3. **Loop ceiling earned, không assumed** — `task-loop` KHÔNG nâng trần pack nào.
4. **Governed universe nguyên vẹn** — đổi tên/ thêm lệnh vẫn phải giải được owner cho mọi
   product path (`EVOLUTION_ORPHAN_PATH`), để `kit-evolve` sau này quản được cả `task-loop`.
5. Telemetry facts immutable; evolution proposal deterministic + review-bound (v7 §2).

## 3. Command model

```text
code-loop            → pack software-dev (như build-loop cũ, đổi tên)
task-loop              → liệt kê non-software active packs, hỏi chọn
task-loop <domain-id>  → resolve descriptor qua Registry Catalog
                     → load work-loop engine + 6 slot của pack (đúng thứ tự)
                     → chạy deliverable/gate/reviewer routing của pack
```

- Cả hai là **thin trigger generated** qua `render.py`; không policy domain trong trigger.
- `task-loop` chỉ route pack `lifecycle=active` và **không phải** `software-dev`; quy tắc loại
  trừ khai trong registry, không hardcode trong trigger.
- **Registry-driven:** pack mới đăng ký `registry/domains.json` → tự vào `task-loop`, không sửa
  skill/shell (extension-proof v7 §9.2).
- `knowledge-work` skill hiện có → redirect-alias tới `task-loop knowledge-work` (giữ thói quen
  cũ tối thiểu một minor), hoặc gập vào `task-loop` — quyết trong Phase B.

## 4. Phases

Mỗi phase append scorecard line. Gate nhẹ theo §6. Reviewer tuần tự, diff-scoped (v7 §16).

### Phase A — Đổi tên `build-loop → code-loop` (giữ alias)
Điểm chạm (đổi qua descriptor → render, không sửa tay generated file):
- `registry/domains.json`: đổi trigger name của `software-dev` thành `code-loop`; thêm
  `aliases: ["build-loop"]` để không phá tài liệu/muscle-memory/plugin cũ.
- Render lại → `skills/code-loop/SKILL.md`; giữ `skills/build-loop/SKILL.md` thành trigger
  redirect (hoặc alias trong metadata) tối thiểu một minor.
- Cập nhật: `.claude-plugin/plugin.json` + `marketplace.json`, `.codex-plugin/`,
  `.agents/plugins/`, `hooks.json` nếu tham chiếu tên; `fable-dat` skill (references
  `build-loop`); README/HUONG_DAN/docs.
- **Fixtures:** trigger-eval positive cho `code-loop` + cho alias `build-loop`; byte-exact
  `--check` pass; hành vi pack software-dev không đổi.
- **Exit:** `code-loop` chạy y như `build-loop`; alias cũ vẫn kích hoạt; projection green.

### Phase B — Lệnh `task-loop` (generated, registry-driven)
- Thêm mô hình "non-software active pack" (trường loại trừ/nhóm) vào registry; khai trong
  `docs/contracts/domain-pack.md`.
- `render.py`: projection `task-loop-trigger` → `skills/task-loop/SKILL.md`.
- Quyết số phận `skills/knowledge-work` (redirect-alias vs gập).
- **Red-before-green fixtures:** (1) synthetic non-software pack → hiện trong `task-loop`, không
  sửa Python/shell; (2) `software-dev` KHÔNG hiện trong `task-loop`; (3) hand-edit trigger fail
  `--check`; (4) load đúng 6 slot của pack được chọn (eval load file thật, không chỉ tên).
- **Exit:** `task-loop` route đúng mọi non-software pack; `code-loop` không đổi; projection
  byte-exact.

### Phase C — Docs sweep + ranh giới hiển nhiên
- README: mục "Hai cửa vào" — `code-loop` (code) / `task-loop` (non-code) — lên đầu.
- `docs/domains.md` + `docs/loops.md`: bảng ranh giới; gỡ từ "final/permanent" còn nợ (ADR
  0001).
- `HUONG_DAN.vi.md`: hướng dẫn tiếng Việt cho cả hai lệnh + alias.
- **Exit:** đọc mô tả là biết ngay build/code=code, do=non-code; trigger-eval pos/neg pass.

### Phase D — (tùy chọn) author một non-code pack thật Dat dùng
- `domain-builder` phỏng vấn Dat → encode một nghề Dat thật sự làm (AI-transformation
  consulting / interview prep / content). Pack thứ 3 tự vào `task-loop`. Ceiling capped
  Turn/Goal.
- **Exit:** một non-code pack chạy end-to-end qua `task-loop`.

### Phase E — Nối lại telemetry-v3 (self-learning) — resume v7 Phase 6
- Tiếp B-line từ **subset #4** (task/handoff linkage: `resumed_from_handoff`, giữ task ID qua
  handoff, parent/delegation) → subset #5 (report views) → B4 (durable export) → B5 (release
  closure). Theo memory `dat-kit-b3-subset3-next`.
- **Bổ sung task-loop vào telemetry:** event ghi `domain-id` để đo cả non-code work, và
  event-coverage-rate cho lệnh `task-loop`.
- **Exit:** năm named producer chạy; telemetry ghi cả code lẫn non-code task; DoD v7 §13.2.

### Phase F — Nối lại evolution (self-evolution) — resume v7 Phase 7
- `kit-evolve` sau khi có active telemetry producer. Governed universe **bao gồm cả `task-loop`
  + các non-code pack** → kit có thể đề xuất cải tiến chính các pack đó.
- Giữ nguyên automation boundary v7: miner sinh proposal + patch trong branch cô lập, **không**
  tự merge / đổi authority / nới policy tự-chứng; self-modification = Class C.
- **Exit:** DoD v7 §13.3 (shadow mode, Class A/B rehearsal, không autonomous merge).

## 5. Điều CỐ Ý không làm (scope guard)

- Không rip registry/projections/engine (đã xong, load-bearing).
- **Không park/xóa telemetry hay evolution** — north star giữ nguyên, chỉ hoãn sau tách lệnh.
- Không nâng loop ceiling pack nào; không autonomous merge trước Phase 8 (v7 giữ nguyên).
- Không marketplace/ontology nghề (out-of-scope v7 §11).
- Không review 3-agent song song (v7 §16: tuần tự, diff-scoped, findings-scoped re-review).

## 6. Gates — bảng quyết định theo rủi ro (THAY THẾ v7 §9.1 cho việc maintain kit)

**Ghi rõ để không mơ hồ:** khi maintain dat-kit, mục này **thay thế** chuỗi review cứng của
v7 §9.1 ("plan audit → QA → code review → conditional security → regression QA" với 4 reviewer
cho *mọi* phase). Chuỗi đầy đủ đó **chỉ còn bắt buộc cho tier D bên dưới**. Lý do: dat-kit chủ
yếu là prompt/markdown/registry + ít script — full pipeline cho mọi diff là cái ngốn ~284k
token/round (v7 §16), không mua thêm an toàn thật. Nguyên tắc: **gate theo rủi ro của thay
đổi, không theo nghi thức.**

| Tier | Loại thay đổi | Gate bắt buộc | qa | code-rev | security |
|---|---|---|---|---|---|
| **A** | Docs / SKILL description / registry JSON không đổi hành vi script | `validate.py` + `render.py --check` byte-exact + trigger-eval pos/neg + invoke thử 1 lần | — | — | — |
| **B** | Trigger/projection đổi hành vi (Phase A rename, Phase B task-loop routing) | Tier A **+** eval load 6 slot file thật + test alias | — | — | — |
| **C** | Script thực thi (`render.py`/`registry.py`/`telemetry.py`) | Tier A + `pytest` + **1 reviewer tuần tự** | có | có¹ | chỉ khi chạm path tùy ý / parse input ngoài² |
| **D** | Evolution `kit-evolve`, hoặc bất kỳ enforcement code nào có thể **nới gate** (Class C) | **Full v7 discipline**: plan audit → QA → code review → security → regression, tuần tự | có | có | **có** |

¹ Một reviewer, diff-scoped, findings ≤ ~30 dòng (v7 §16 rules 2–4). Không 3-agent song song.
² Ví dụ tier-C cần security: TSV manifest parsing, telemetry export path, bất kỳ chỗ input đi
vào path/shell → traversal/injection.

**Sàn luôn-bật (không tier nào được bỏ):**
- **Regression hành vi skill** — mỗi lần đổi description/trigger PHẢI có trigger-eval cập nhật.
  Đây là rủi ro riêng của một *tool*: skill hỏng phá âm thầm mọi project downstream. Là
  *consistency*, không phải security. Cực quan trọng ở Phase A (**đổi tên** → test cả tên mới
  lẫn alias cũ).
- **Reviewer luôn tuần tự + diff-scoped** (không bao giờ song song, không đọc cả repo).
- Mỗi phase append một scorecard line.

**Vì sao security vẫn còn ở C²/D** (không mâu thuẫn với "gate nhẹ"): không phải để chống
hacker, mà chống hai rủi ro thật của tool — (a) input parsing đi vào path/shell, (b) `kit-evolve`
tự sửa mình và có thể hạ gaming-line / tự-chứng bằng eval nó vừa tạo (cần temporal-independence,
Class C). Đây là "gate của gate", cố ý giữ nghiêm.

## 7. Migration & tương thích

- **Đổi tên là điểm rủi ro nhất:** `build-loop` giữ làm alias/redirect tối thiểu một minor;
  test cả tên mới lẫn alias. Cập nhật mọi manifest host (`.claude-plugin`, `.codex-plugin`,
  `.agents/plugins`) + install docs.
- `task-loop` là bổ sung, không breaking. `knowledge-work` giữ redirect-alias nếu gập.
- Generated projects v2.0 không breaking.
- telemetry/evolution resume từ điểm green hiện tại; memory `dat-kit-b3-subset3-next` là điểm
  vào Phase E.

## 8. Định nghĩa hoàn thành (v8)

- [ ] `build-loop` đổi thành `code-loop`; alias `build-loop` vẫn kích hoạt; hành vi software-dev
      không đổi; projection green.
- [ ] `task-loop` là generated thin trigger; route đúng mọi non-software active pack; synthetic
      pack hiện không sửa code/shell; `software-dev` không lọt vào.
- [ ] Docs (README + domains + loops + HUONG_DAN.vi) nhất quán; "final/permanent" đã gỡ.
- [ ] (tùy chọn) một non-code pack thật chạy end-to-end qua `task-loop`.
- [ ] telemetry-v3 nối lại và đóng (DoD v7 §13.2), ghi cả code lẫn non-code task.
- [ ] evolution nối lại và đóng (DoD v7 §13.3); governed universe phủ cả `task-loop` + pack mới.
- [ ] Gate theo §6 pass mỗi phase; mỗi phase một scorecard line.

## 9. Model selection theo bước (nhất quán với `docs/model-selection.md`)

Nguyên tắc gốc giữ nguyên: **chọn model theo *cái giá của việc sai*, không theo độ tẻ nhạt của
việc**. Controller (session chạy loop) là tier cao nhất đang chơi; worker làm việc cơ học thì
rẻ nhất mà vẫn đúng. Bảng dưới là gợi ý cho từng bước v8:

| Bước | Model đề xuất | Vì sao |
|---|---|---|
| Phase A — bulk rename qua manifest/docs (find-replace `build-loop`→`code-loop`) | **haiku** | Cơ học, độc lập, khối lượng lớn, thấp rủi ro. Nhưng **verify alias** bằng eval (sàn §6). |
| Phase A — sửa descriptor `registry/domains.json` + render lại | **sonnet** | Bounded, theo pattern projection có sẵn. |
| Phase B — thiết kế exclusion rule + contract `domain-pack.md` cho task-loop | **opus** | Cần judgment kiến trúc (governed universe, loại trừ software-dev) — sai thì lệch cả model. |
| Phase B — code `render.py` projection `task-loop-trigger` | **sonnet** | Bounded, mở rộng renderer sẵn có. |
| Phase C — docs sweep (README/domains/loops/HUONG_DAN) | **sonnet** | Prose theo cấu trúc rõ; không cần opus. |
| Phase D — `domain-builder` phỏng vấn + encode pack non-code | **opus** | Encode discipline của một nghề + gate-validity là judgment thật. |
| Phase E — code telemetry subset #4+ (`telemetry.py`) | **sonnet** | Bounded, tiếp pattern B-line hiện có. |
| Phase F — code `kit-evolve` (evolution engine) | **opus** | Enforcement code nới được gate (Class C); design + an toàn đắt khi sai. |
| **Reviewer mọi tier** (qa/code/security/plan) | **opus** (pin sẵn trong `agents/*.md`) | Vai trò judge/verify/audit — giữ nguyên pin. |
| Consult dispatch khi bí bất ngờ (gate đỏ sau retry, hết hypothesis) | **opus→fable** qua per-invocation param | Bất ngờ khó, không pin cứng; log vào `benchmarks/escalations.jsonl`. |

**Quy tắc kèm theo (từ policy, nhắc lại để khỏi trượt):**
- **KHÔNG đổi reviewer `model:` pin** trong v8 — đó là Class C, chỉ đổi trên per-reviewer
  evidence của v2.1 (v7 §11, §16 rule 7). Muốn một review nặng hơn tier session → raise *một*
  dispatch bằng per-invocation `model`, đừng sửa file agent.
- **fable không pin trong agent file** (availability/chi phí) — chỉ raise per-dispatch khi một
  bước thật sự cần judgment vượt opus.
- **Codex host:** dat-kit không claim schema model-routing của Codex; dùng cùng role charter
  với subagent tươi, để Codex tự chọn tier. Reviewer fallback vẫn bắt buộc cả hai host.
- Nếu session chính đang chạy **dưới** tier một bước cần (vd audit security trên sonnet) → t sẽ
  nói và đề nghị bạn `/model` nâng lên, không âm thầm hạ chất lượng audit.

---

**Ghi chú thực thi:** đây là *plan*, chưa phải lệnh chạy. Duyệt xong t đề nghị bắt đầu **Phase
A (đổi tên)** vì mọi thứ sau dựa trên tên mới ổn định; telemetry/evolution nối lại ở E–F.
