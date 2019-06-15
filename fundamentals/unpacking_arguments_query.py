"""
This file is good example when use **kargs
"""


def create_statement(type_metric, **kargv):
    """
    :param type_metric: choose table
    :param argv: all metrics to records
    :return: statement of INSERT INTO
    """
    if type_metric == "jobs":
        return "INSERT INTO jobs " \
               "(execution_date, job_name, job_status," \
               " start_time, end_time, execution_time, fk_module) " \
               "VALUES " \
               "('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}');" \
            .format(kargv['execution_date'],
                    kargv['job_name'],
                    kargv['status'],
                    kargv['start_time'],
                    kargv['end_time'],
                    kargv['execution_time'],
                    kargv['fk_module'])
    else:
        return "INSERT INTO modules " \
               "(execution_date, module_name, module_status," \
               " start_time, end_time, execution_time) " \
               "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}');" \
            .format(kargv['execution_date'],
                    kargv['module_name'],
                    kargv['status'],
                    kargv['start_time'],
                    kargv['end_time'],
                    kargv['execution_time'])


if __name__ == '__main__':
    create_statement(type_metric='modules',
                     execution_date='2020-01-01',
                     module_name='search',
                     status='SUCESS',
                     start_time='15:00',
                     end_time='16:30',
                     execution_time='1:30')
