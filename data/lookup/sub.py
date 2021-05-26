import io
f = open("problem_title.txt", 'r+')

line = f.readlines()
lines = [line[i] for i in range(len(line)) if i % 3 == 1]
print(lines)


f.close()


f = open("problem_title2.txt", 'w')

for i in lines:
    f.write(i)

f.close()


# ## intent:past
# - [지난](past)
# - [지난번](past)
# - [저번](past)
# - [저번](past)에
# - [예전](past)
# - [예전](past)에
# - [과거](past)
# - [과거](past)에
#
# ## intent:one_year_ago
# - 1년전
# - 1년 전
# - 작년
# - 작년에
# - 저번 년도
# - 지난 해
# - 전해
# - 거년
# - 지난해
# - 지난해에
#
# ## intent:two_year_ago
# - 2년전
# - 2년 전
# - 재작년
# - 재작년에
# - 재작년도
# - 저저번년도
# - 저저번해
#
# ## intent:three_year_ago
# - 3년전
# - 3년 전
# - 재재작년
# - 재재작년에
#
# ## intent:proceeding
# - 지금
# - 현재
# - 진행중
# - 진행 중
# - 하고있는
# - 열려있는
# - 진행중인
# - 참가가능한
# - 참가 가능한
# - 열린
# - 지원 가능한
# - 지원할 수 있는
# - 참여할 수 있는
# - 참여할
#
# ## intent:expected
# - 최근
# - 요즘
# - 요즘에
# - 곧
# - 다음번에
# - 다음에
# - 곧 열리는
# - 열릴 예정인
# - 나중에