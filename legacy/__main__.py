import runpy
import sys

# Делаем вид, что команда была "python3 -m hikka"
sys.argv[0] = "legacy"

# Запускаем hikka так, как будто её вызвали напрямую
runpy.run_module("legacy", run_name="__main__")
