概述：
	实现了左递归消除
	py2环境下运行。
源文件：
	Analysis.py。
	主程序结构如下。
def main():
    c=compiler()
    c.get_productions()#获取生产式
    c.eliminate_left_recursive()#去除直接左递归。可注释该行。
    c.calc_first()#计算first集合
    c.calc_follow()#计算follow集合
    c.calc_table()#计算预测分析表
    c.output_table()#输出预测分析表
输入文件：
	syntax.txt
	每行含一个产生式，第一行为开始符号的一个产生式。各符号间以空格分割。“empty”与"$"为保留字。
	输入的文法中无间接左递归。
输出文件：
	predict_table.txt
	预测分析表。
	若产生式总长超过20个字符可能出现格式错乱。