# CI-Maintenance Simplification Measurements

Counts use LF-normalized canonical files, Unicode whitespace-separated words, UTF-8 bytes, and each unique packaged resource once. External project contracts and approved designs are disclosed but excluded.

| Assembly | Before words | After words | Before bytes | After bytes |
| --- | ---: | ---: | ---: | ---: |
| CIM0 narrow review | 1369 | 890 | 9653 | 7410 |
| CIM1 ordinary revise | 1369 | 1146 | 9653 | 9440 |
| CIM1 create/structural replace | 1522 | 1211 | 11290 | 10050 |
| CIM2 project-native file | 1369 | 890 | 9653 | 7410 |
| CIM3 external-state route | 1369 | 890 | 9653 | 7410 |
| CIM4 invalid stop | 1369 | 890 | 9653 | 7410 |
| CIM5 coverage review | 1861 | 1217 | 12758 | 9509 |
| CIM6 coverage revise | 1861 | 1473 | 12758 | 11539 |
| CIM6 coverage create | 2014 | 1538 | 14395 | 12149 |
| CIM7 privileged review | 1369 | 890 | 9653 | 7410 |
| CIM8 privileged revise | 1369 | 1146 | 9653 | 9440 |
| CIM8 privileged create | 1522 | 1211 | 11290 | 10050 |
| CIM8 coverage revise | 1861 | 1473 | 12758 | 11539 |
| CIM8 coverage create | 2014 | 1538 | 14395 | 12149 |
| Complete package | 2014 | 1538 | 14395 | 12149 |

Final resources: root 890/7410; GitHub reference 256/2030; risk map 327/2099; skeleton 65/610. Every supported assembly strictly decreases in both measures.

