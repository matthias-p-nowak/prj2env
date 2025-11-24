pypi:
    rm -frv dist
    uv build
    uvx twine upload dist/prj2env*.whl

testpypi:
    rm -frv dist
    uv build
    uvx twine upload --repository testpypi dist/prj2env*.whl