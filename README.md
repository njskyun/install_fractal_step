## op_cat 按照之前教程不是从0区块同步数据的，解决打所有token方案
  
```操作步骤
cd /var
git clone https://github.com/njskyun/install_fractal_step.git
sudo -i -u postgres
psql -U postgres -d 数据库名(默认安装没动过就填： postgres)
\i /var/install_fractal_step/block_74600_token_info.sql

等1分钟不到，出现“ALTER TABLE”字样，继续下一步
\q
切换到root账号，su root
优点：节省时间，从最新块开始同步数据都可以
缺点：由于你的块太新，会提示找不到minter，不过等别人mint后过一个块后，就可以了跟着跑了
```
