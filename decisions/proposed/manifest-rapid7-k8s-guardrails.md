## Environment
- default branch: main; protected: main
- contents: dockerfile image build
- pipeline: .gitlab-ci.yml; stages: test, secret-detection  # .gitlab-ci.yml:8
- source: CI include template Security/Secret-Detection.gitlab-ci.yml; git cannot see this  # .gitlab-ci.yml:16
