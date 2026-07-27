# Tang OS Quick Start v1.0

**10分钟运行 Tang OS Reference Implementation.**

---

## 安装

```bash
pip install tang-os
```

或从源码安装：

```bash
git clone https://github.com/tang-os/tang-os.git
cd tang-os
pip install -e .
```

## 验证安装

```bash
python run_conformance.py
```

预期输出：`Overall: ✅ CONFORMANT`

## 基本使用

```python
from tang_os import Tang

tang = Tang()
result = tang.process("我今天很难过")

print(result["emotional_state"].feeling)
# → Feeling.SADNESS

print(result["response_decision"].candidate_intent)
# → "acknowledge"
```

## 创建 Extension

```python
from tang_os_sdk import TangExtension, ManifestValidator

ext = TangExtension("my_extension", "实现自定义能力")
ext.set_category("C2")
ext.set_authority_level("A1")
ext.add_permission("knowledge_query")

manifest = ext.build()
print(ManifestValidator().validate(manifest))
# → {"valid": True, "errors": []}
```

## 运行沙箱测试

```python
from tang_os_sdk import SandboxAPI

sandbox = SandboxAPI()
sandbox.run_scenario("benign_interaction")     # ✅
sandbox.run_scenario("prescribed_decision")    # ✅ Rejected
```

## 验证 Extension 兼容性

```python
from tang_os_sdk import ConformanceRunner

results = ConformanceRunner().run_all()
assert results["success"]
```

## 下一步

- 阅读 [Specification](docs/09_public_specification/TANG_OS_SPECIFICATION_v1.0.md)
- 浏览 [Examples](examples/)
- 查看 [API Reference](API_REFERENCE.md)
