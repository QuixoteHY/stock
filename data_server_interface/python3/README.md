# 使用说明
```text
默认服务器：119.29.152.194
默认端口：8888

例子：http://119.29.152.194:8888/get/stock/fina_indicators/600699
```

## 一、Web接口API

### API说明：

- {financial_statement_type}：财务数据类型
- {ts_code}：股票代码

#### 获取某股票的财务数据
```text
/get/stock/{financial_statement_type}/{ts_code}
```

##### 例子：
- http://119.29.152.194:8888/get/stock/fina_indicators/{ts_code} 获取股票代码为{ts_code}的财务指标
