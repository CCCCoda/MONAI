# Copyright 2020 MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import numpy as np
import torch
from parameterized import parameterized

from monai.transforms import RandAffined

TEST_CASES = [
    [
        dict(as_tensor_output=False, device=None, spatial_size=(2, 2), keys=('img', 'seg')),
        {'img': torch.ones((3, 3, 3)), 'seg': torch.ones((3, 3, 3))},
        np.ones((3, 2, 2))
    ],
    [
        dict(as_tensor_output=True, device=None, spatial_size=(2, 2, 2), keys=('img', 'seg')),
        {'img': torch.ones((1, 3, 3, 3)), 'seg': torch.ones((1, 3, 3, 3))},
        torch.ones((1, 2, 2, 2))
    ],
    [
        dict(prob=0.9,
             rotate_range=(np.pi / 2,),
             shear_range=[1, 2],
             translate_range=[2, 1],
             as_tensor_output=True,
             spatial_size=(2, 2, 2),
             device=None,
             keys=('img', 'seg'),
             mode='bilinear'), {'img': torch.ones((1, 3, 3, 3)), 'seg': torch.ones((1, 3, 3, 3))},
        torch.tensor([[[[0.0000, 0.6577], [0.9911, 1.0000]], [[0.7781, 1.0000], [1.0000, 0.4000]]]])
    ],
    [
        dict(prob=0.9,
             rotate_range=(np.pi / 2,),
             shear_range=[1, 2],
             translate_range=[2, 1],
             scale_range=[.1, .2],
             as_tensor_output=True,
             spatial_size=(3, 3),
             keys=('img', 'seg'),
             device=None), {'img': torch.arange(64).reshape((1, 8, 8)), 'seg': torch.arange(64).reshape((1, 8, 8))},
        torch.tensor([[[16.9127, 13.3079, 9.7031], [26.8129, 23.2081, 19.6033], [36.7131, 33.1083, 29.5035]]])
    ],
    [
        dict(prob=0.9,
             mode=('bilinear', 'nearest'),
             rotate_range=(np.pi / 2,),
             shear_range=[1, 2],
             translate_range=[2, 1],
             scale_range=[.1, .2],
             as_tensor_output=False,
             spatial_size=(3, 3),
             keys=('img', 'seg'),
             device=torch.device('cpu:0')),
        {'img': torch.arange(64).reshape((1, 8, 8)), 'seg': torch.arange(64).reshape((1, 8, 8))},
        {'img': np.array([[[16.9127, 13.3079, 9.7031], [26.8129, 23.2081, 19.6033], [36.7131, 33.1083, 29.5035]]]),
         'seg': np.array([[[19., 12., 12.], [27., 20., 21.], [35., 36., 29.]]])}
    ],
]


class TestRandAffined(unittest.TestCase):

    @parameterized.expand(TEST_CASES)
    def test_rand_affined(self, input_param, input_data, expected_val):
        g = RandAffined(**input_param).set_random_state(123)
        res = g(input_data)
        for key in res:
            result = res[key]
            expected = expected_val[key] if isinstance(expected_val, dict) else expected_val
            self.assertEqual(torch.is_tensor(result), torch.is_tensor(expected))
            if torch.is_tensor(result):
                np.testing.assert_allclose(result.cpu().numpy(), expected.cpu().numpy(), rtol=1e-4, atol=1e-4)
            else:
                np.testing.assert_allclose(result, expected, rtol=1e-4, atol=1e-4)


if __name__ == '__main__':
    unittest.main()
