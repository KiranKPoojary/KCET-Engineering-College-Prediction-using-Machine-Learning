#include <stdio.h>
// void swap(int a[],int ak, int bk)
// {
//     int temp = a[ak];
//     a[ak] = a[bk];
//     a[bk] = temp;
// }

int part(int a[],int lb,int ub)
{
    int pivot=a[lb];
    int start=lb+1;
    int end=ub;
    while(lb<=ub)
    {
        if(a[start]<=pivot)
        {
            start++;
        }
        if(a[start]>pivot)
        {
            end--;
        }
        if(start<=end)
        {
          int temp=a[start];
          a[start]=a[end];
          a[end]=temp;
        }
    }
  
  int temp=a[lb];
  a[lb]=a[end];
  a[end]=temp;

    return end;
}

void quick(int a[],int lb,int ub)
{
    if(lb<ub)
    {
        int pos=part(a,lb,ub);
        quick(a,lb,pos-1);
        quick(a,pos+1,ub);
    }
}

void main()
{
    int a[20],n,i;
    printf("Enter number of integers\n");
    scanf("%d",&n);
    printf("Enter element\n");
    for(i=0;i<n;i++)
    {
        scanf("%d",&a[i]);
    }
    quick(a,0,n-1);
    printf("after quick sort\n");
    for(i=0;i<n;i++)
    {
        printf("%d",a[i]);
    }
}  