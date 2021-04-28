import numpy as np
from util.features import prepare_for_training


class LinearRegression:
    def __init__(self, data, labels, polynomial_degree=0, sinusoid_degree=0, normalize_data=True):
        """：
        1.对数据进行预处理操作
        2.先得到所有的特征个数
        3.初始化参数矩阵

        data:数据
        polynomial_degree: 是否做额外变换
        sinusoid_degree: 是否做额外变换
        normalize_data: 是否标准化数据
        """
        (data_processed,
         features_mean,
         features_deviation) = prepare_for_training.prepare_for_training(data, polynomial_degree, sinusoid_degree,
                                                                         normalize_data)

        self.data = data_processed
        self.labels = labels
        self.features_mean = features_mean
        self.features_deviation = features_deviation
        self.polynomial_degree = polynomial_degree
        self.sinusoid_degree = sinusoid_degree
        self.normalize_data = normalize_data

        num_features = self.data.shape[1]
        self.theta = np.zeros((num_features, 1))

    def train(self, alpha, num_iterations=500):
        """
        训练模块，执行梯度下降得到theta值和损失值loss

        alpha: 学习率
        num_iterations: 迭代次数
        """
        cost_history = self.gradient_descent(alpha, num_iterations)
        return self.theta, cost_history

    def gradient_descent(self, alpha, num_iterations):
        """
        实际迭代模块

        alpha: 学习率
        num_iterations: 迭代次数

        :return: 返回损失值 loss
        """
        cost_history = []  # 收集每次的损失值
        for _ in range(num_iterations):  # 开始迭代
            self.gradient_step(alpha)  # 每次更新theta
            cost_history.append(self.cost_function(self.data, self.labels))
        return cost_history

    def gradient_step(self, alpha):
        """
        梯度下降参数更新计算方法，注意是矩阵运算

        alpha: 学习率
        """
        num_examples = self.data.shape[0]  # 当前样本个数
        # 根据当前数据和θ获取预测值
        prediction = LinearRegression.hypothesis(self.data, self.theta)
        delta = prediction - self.labels  # 残差，即预测值减去真实值
        theta = self.theta
        # 依照小批量梯度下降法，写代码表示
        theta = theta - alpha * (1/num_examples)*(np.dot(delta.T, self.data)).T
        self.theta = theta  # 计算完theta后更新当前theta

    def cost_function(self, data, labels):
        """
        损失计算方法，计算平均的损失而不是每个数据的损失值
        """
        num_examples = data.shape[0]
        delta = LinearRegression.hypothesis(data, self.theta) - labels  # 预测值-真实值 得到残差
        cost = np.dot(delta, delta.T)  # 损失值
        return cost[0][0]

    @staticmethod
    def hypothesis(data, theta):
        """
        获取预测值

        :param data:  矩阵数据
        :param theta:  权重θ
        :return: 返回预测值
        """
        predictions = np.dot(data, theta)
        return predictions

    def get_cost(self, data, labels):
        """
        得到当前损失
        """
        data_processed = prepare_for_training.prepare_for_training(data,
                                                                   self.polynomial_degree,
                                                                   self.sinusoid_degree,
                                                                   self.normalize_data)[0]
        return self.cost_function(data_processed, labels)

    def predict(self, data):
        """
        用训练的参数模型，预测得到回归值的结果
        """
        data_processed = prepare_for_training.prepare_for_training(data,
                                                                   self.polynomial_degree,
                                                                   self.sinusoid_degree,
                                                                   self.normalize_data)[0]
        predictions = LinearRegression.hypothesis(data_processed, self.theta)

        return predictions
