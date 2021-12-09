from django.http import request
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connections

@api_view(['GET'])
def retrieve_data(request):
    department = request.GET.get('department')
    print(department)
    args = department.upper()
    sql = """SELECT edt."Employee Name	" from public."Employee Detail Table	" edt
    INNER JOIN public."DepartmentTable	" dt ON dt."DepartmentID	" = edt."DepartId"
    where UPPER(dt."DepartmentName	")= %(department)s """
    cur = connections['default'].cursor()
    cur.execute(sql,{"department": args})
    emp_list = []
    for row in cur:
        emp_list.append(row[0])
    cur.close()
    return JsonResponse(emp_list, safe=False)
@api_view(['POST','GET'])
def create(request):
    var = 99999999
    department = request.data['department']
    dept_sql = """SELECT "DepartmentID	" from public."DepartmentTable	" ORDER BY "DepartmentID	" DESC LIMIT 1"""
    cur = connections['default'].cursor()
    cur.execute(dept_sql)
    deptId = ""
    for row in cur:
       deptId = row[0]
    cur.close()
    print(deptId[3:len(deptId)])
    cur_id = int(deptId[3:len(deptId)])
    if cur_id < var:
        cur_id = cur_id + 1
    len_cur_id = len(str(cur_id))
    inc_str = ""
    
    for i in range(0,8-len_cur_id):
        inc_str = inc_str + "0"
    req_inc = "DEP"+inc_str+str(cur_id)

    ins_sql = """INSERT INTO public."DepartmentTable	" ("DepartmentID	","DepartmentName	") VALUES (%(deptId)s,%(deptName)s)"""
    cur = connections['default'].cursor()
    status = "Unable to create records"
    try:
        cur.execute(ins_sql,{"deptId": req_inc, "deptName": department})
        status = "Created successfully"
    except Exception as e:
        print(e)
    cur.close()

    return JsonResponse(status, safe=False)    

