# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path

from ..examples.test_plan import prepare_files
from ..examples.utils import get_tftest_directive

BASE_PATH = Path(__file__).parent


def test_example(e2e_validator, tmp_path, examples_e2e,
                 e2e_tfvars_path_session):
  (tmp_path / 'fabric').symlink_to(BASE_PATH.parents[1])
  (tmp_path / 'variables.tf').symlink_to(BASE_PATH.parent / 'examples' /
                                         'variables.tf')
  (tmp_path / 'main.tf').write_text(examples_e2e.code)
  assets_path = BASE_PATH.parent / str(examples_e2e.module).replace(
      '-', '_') / 'assets'
  if assets_path.exists():
    (tmp_path / 'assets').symlink_to(assets_path)
  (tmp_path / 'terraform.tfvars').symlink_to(e2e_tfvars_path_session)

  # add files the same way as it is done for examples
  directive = get_tftest_directive(examples_e2e.code)
  if directive and directive.name == 'tftest':
    prepare_files(examples_e2e, tmp_path, directive.kwargs.get('files'),
                  directive.kwargs.get('fixtures'))

  e2e_validator(module_path=tmp_path, extra_files=[],
                tf_var_files=[(tmp_path / 'terraform.tfvars')])


# use a function scoped fixture, so for each test gets a brand-new test project
# Some tests (especially PSA), which use abandon strategy when removing, leave the project in
# unclean state, which may prevent successful completion of the next test.
# This allows marking such cases as isolated, and those tests will get a separate project, which won't be reused
# for other tests
def test_isolated_example(e2e_validator, tmp_path, examples_e2e,
                          e2e_tfvars_path_function):
  return test_example(e2e_validator, tmp_path, examples_e2e,
                      e2e_tfvars_path_function)
